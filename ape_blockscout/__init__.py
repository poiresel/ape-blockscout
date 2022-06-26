from ape import plugins

from .explorer import Blockscout

NETWORKS = {
    "ethereum": [
        "mainnet",
    ],
    "ethereum-classic": [
        "mainnet",
    ],
    "xdai": [
        "mainnet",
        "aox",
        "optimism",
        "testnet",
    ],
    "poa": [
        "core",
        "sokol",
    ],
}


@plugins.register(plugins.ExplorerPlugin)
def explorers():
    for ecosystem_name in NETWORKS:
        for network_name in NETWORKS[ecosystem_name]:
            yield ecosystem_name, network_name, Blockscout
            yield ecosystem_name, f"{network_name}-fork", Blockscout