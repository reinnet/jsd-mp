import dataclasses


@dataclasses.dataclass(frozen=True)
class VNFM:
    """
    VNFM class contains the information about VNFMs.
    Each VNFM uses 'cores' and 'memory' from the deployed node
    and can manage the 'capacity' functions.
    """

    cores: int
    memory: int
    capacity: int
    radius: int
    bandwidth: int
    license_cost: int
