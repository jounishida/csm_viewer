class ViewManager:

    def __init__(self):

        self.views = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None
        }

    def save_view(
        self,
        slot,
        camera
    ):

        self.views[
            slot
        ] = (
            camera.save_state()
        )

    def has_view(
        self,
        slot
    ):

        return (
            self.views.get(slot)
            is not None
        )

    def restore_view(
        self,
        slot
    ):

        return self.views[
            slot
        ]

