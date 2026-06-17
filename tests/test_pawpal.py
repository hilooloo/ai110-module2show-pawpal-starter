from pawpal_system import Task, Pet


def test_mark_complete_sets_is_completed_true():
    task = Task(description="Morning walk", time_str="07:30", frequency="daily")
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(description="Feeding", time_str="08:00", frequency="daily"))
    assert len(pet.tasks) == 1
