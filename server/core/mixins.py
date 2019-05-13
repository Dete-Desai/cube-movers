from .models import Move, Checklist


class GetMoveObjMixin():
    def get_object(self, queryset=None):
        if not self.obj:
            move_id = self.kwargs.get(self.pk_url_kwarg)
            self.obj = Move.objects.get(id=move_id)
        return self.obj


class GetChecklistObjMixin():
    def get_object(self, queryset=None):
        if not self.obj:
            checklist_id = self.kwargs.get(self.pk_url_kwarg)
            self.obj = Checklist.objects.get(pk=checklist_id)
        return self.obj
