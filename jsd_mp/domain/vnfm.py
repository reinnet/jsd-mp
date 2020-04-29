import dataclasses


@dataclasses.dataclass(frozen=True)
class VNFM:
    cores: int
    memory: int
    capacity: int
    radius: int
    bandwidth: int
    license_cost: int
