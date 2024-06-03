import os

SLOTS_DATA_PATH = os.path.join(os.path.dirname(__file__), "slots_data")

URL_ULTRASOUND = "https://relay-analytics.ultrasound.money"
URL_FLASHBOTS = "https://boost-relay.flashbots.net"

FLASHBOTS_BUILDERS = {
    "plain": [
        "0xa01a00479f1fa442a8ebadb352be69091d07b0c0a733fae9166dae1b83179e326a968717da175c7363cd5a13e8580e8d",
        "0xa01b00a4ab433cbb0a0801cff3815722d56e1980caad7ed156900563e6670cdf6280535dae331f358c647c4bf4558a85",
        "0xa02a0054ea4ba422c88baccfdb1f43b2c805f01d1475335ea6647f69032da847a41c0e23796c6bed39b0ee11ab9772c6",
        "0xa02b009596e741d5f61d18b900cbd03bbcdb9c0f16b1981928d13b57fcb48d4ddce21a96c523bf84425b3a4e6e6b3f14",
        "0xa03a000b0e3d1dc008f6075a1b1af24e6890bd674c26235ce95ac06e86f2bd3ccf4391df461b9e5d3ca654ef6b9e1ceb",
        "0xa03b00ddb78b2c111450a5417a8c368c40f1f140cdf97d95b7fa9565467e0bbbe27877d08e01c69b4e5b02b144e6a265",
        "0xa08a00b8d1521ddc7e51717f9e1ed77266108008acec8cb58aa492ed0a17cc4c55330cfb1871d4471a7451d3f7c89192",
        "0xa08b00cedceeb18c97d723f9338ead7d660fffc9050e487a5219e334e08e3d15faf4d8b51b0daf0e792f5f27a8c54da0",
    ],
    "tdx": [
        "0x800a002dd9e1afc77af8ae909cf7f8169b413a92cfd43caa56ac749024774d9817a806dae49f4bd5af0661b054595ea4",
        "0x800b00c6e03a92b910cfe928fe6d5bff63eb326af308a6224c512a82c6fdeae92e4d3a39e7b8dbfc572af5d2411cb26c",
        "0x801a00923e9949a7c510f565d92d282bcc79d79da6d57c98972891553443877ba5905b8bdf8145e23a06dac45b9a4d69",
        "0x801b00e0e3a828ef58174652bc74cc6695fee2c7035a935b739c59cdd958c69564668ca5334dc51a85421eba77f9acc2",
        "0x802b00ecf62b2968050b7f557f8edbcbc080c9ee0cecc0982736d85997d3a1fb586587de7fb360fa31bade77254ce2e4",
        "0x802a0012e4878385fbb8fb1f4b7d2ddaf332d2c409d340e2328a75e2387edafd16d543ca07ec2cc8d6134415e5a5b0ad",
    ],
    "sgx": [
        "0x8d333ca548a12676c93dc12cbe650fdfd62284b85f0a60cf68fb33ece035aea18fc1df0057cbe085db0dc593c47b8f4a",
    ],
}

RELAYS = {
    "ultrasound": URL_ULTRASOUND,
    "flashbots": URL_FLASHBOTS,
    "bloxroute": "https://0x8b5d2e73e2a3a55c6c87b8b6eb92e0149a125c852751db1422fa951e42a09b82c142c3ea98d0d9930b056a3bc9896b8f@bloxroute.max-profit.blxrbdn.com",
    "agnostic": "https://0xa7ab7a996c8584251c8f925da3170bdfd6ebc75d50f5ddc4050a6fdc77f2a3b5fce2cc750d0865e05d7228af97d69561@agnostic-relay.net",
    "eden": "https://0xb3ee7afcf27f1f1259ac1787876318c6584ee353097a50ed84f51a1f21a323b3736f271a895c7ce918c038e4265918be@relay.edennetwork.io",
    "aestus": "https://0xa15b52576bcbf1072f4a011c0f99f9fb6c66f3e1ff321f11f461d15e31b1cb359caa092c71bbded0bae5b5ea401aab7e@aestus.live",
    "titan": "https://0x8c4ed5e24fe5c6ae21018437bde147693f68cda427cd1122cf20819c30eda7ed74f72dece09bb313f2a1855595ab677d@titanrelay.xyz",
}
