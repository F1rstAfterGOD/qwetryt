from aiogram.fsm.state import State, StatesGroup

class TaskStates(StatesGroup):
    S_WAIT_LINK = State()
    S_WAIT_WM = State()
    S_WM_TUNE = State()
    S_SUBMITTING = State()