import bpy

class ModalManager:
    modal_stack = []  # Pile pour gérer les opérateurs modaux

    @classmethod
    def add_modal(cls, operator):
        cls.modal_stack.append(operator)
        print(f"Added operator: {operator.bl_idname}")
        cls.print_stack()

    @classmethod
    def remove_modal(cls, operator=None):
        if operator is None and cls.modal_stack:
            # Supprime le dernier opérateur ajouté
            removed_operator = cls.modal_stack.pop()
            print(f"Cancelled operator: {removed_operator.bl_idname}")
            return removed_operator
        elif operator in cls.modal_stack:
            cls.modal_stack.remove(operator)
            print(f"Removed operator: {operator.bl_idname}")
            return operator
        cls.print_stack()
        return None

    @classmethod
    def cancel_last_modal(cls,finish = False):
        # Force l'annulation du dernier opérateur actif
        if cls.modal_stack:
            last_operator = cls.modal_stack.pop()
            print(f"Cancelled operator: {last_operator.bl_idname}")
            # Appeler `removeDialog` si nécessaire
            last_operator.removeDialog()
            if finish:
                return {'FINISHED'}
            else:
                return {'CANCELLED'}
        return {'PASS_THROUGH'}

    @classmethod
    def is_last(cls, operator):
        # Retourne True si l'opérateur donné est le dernier de la pile
        return cls.modal_stack and cls.modal_stack[-1] is operator

    @classmethod
    def print_stack(cls):
        print("Current modal stack (top is last):")
        for op in reversed(cls.modal_stack):
            print(f" - {op.bl_idname}")
