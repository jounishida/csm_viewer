from models.mocap_data import (
    MocapData
)


def load_mocap(
    filename
):

    mocap = MocapData()

    mocap.load_file(
        filename
    )

    return mocap
