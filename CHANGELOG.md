# Changelog

## [1.3.0](https://github.com/ishidawataru/xcvr-emu/compare/v1.2.0...v1.3.0) (2025-04-15)


### Features

* **base:** support parting a table with conditional register definitions ([9e1aad6](https://github.com/ishidawataru/xcvr-emu/commit/9e1aad6b8f1ff3699973d48b02e0fcf78bcee08c))
* **cmis:** add MemMap.with_bank() for easier bank access ([e711c47](https://github.com/ishidawataru/xcvr-emu/commit/e711c47a6ba39d03765ba2804ed06ebdc627e641))
* **cmis:** support loading optoe eeprom hexdump ([b6f99d6](https://github.com/ishidawataru/xcvr-emu/commit/b6f99d648f7b70c107da1f65d78c40171ee7d699))
* initial conditional register definition ([e980f4d](https://github.com/ishidawataru/xcvr-emu/commit/e980f4dd50b64bde253b2662283c8064157de4eb))
* support generating Python classes for conditional registers ([b2da96b](https://github.com/ishidawataru/xcvr-emu/commit/b2da96b9f7d8b4c15e2422f33d45df44f7e2344a))


### Bug Fixes

* silence mypy ([3c08c74](https://github.com/ishidawataru/xcvr-emu/commit/3c08c74c8585d12f2191a8c9192a06898361b0ce))
* when handler needs to take index if the field is ranged ([b19699d](https://github.com/ishidawataru/xcvr-emu/commit/b19699d7e2ef980ba9380b5f7cfe69265c5e6a64))

## [1.2.0](https://github.com/ishidawataru/xcvr-emu/compare/v1.1.0...v1.2.0) (2025-04-07)


### Features

* add Docker image testing and improve Dockerfile for development ([f04622d](https://github.com/ishidawataru/xcvr-emu/commit/f04622dcfd268da36dcdb100da6c5b69296c7f76))
* **client:** bank support ([0184893](https://github.com/ishidawataru/xcvr-emu/commit/01848938822b408f645763cc1cb0e9c29a26b1ee))
* **proto:** add bank field to DataPathStateMachine ([c9a9935](https://github.com/ishidawataru/xcvr-emu/commit/c9a993531080d113a8b8fbda181dd19762325277))
* **server:** bank support ([7ecec98](https://github.com/ishidawataru/xcvr-emu/commit/7ecec983f30a8022d6dcea370d51c07915e67e96))
* **server:** PageSelect, BankSelect field emulation ([7bf4943](https://github.com/ishidawataru/xcvr-emu/commit/7bf4943949c273724edc7674f25019b9dc3f56fb))


### Bug Fixes

* adjust platform settings for pull request builds in workflow ([ffa24c3](https://github.com/ishidawataru/xcvr-emu/commit/ffa24c38d2e25f146fa13f0d338f91bbfb01bf14))
* allow RESERVED value to be appeared once ([ef1c59d](https://github.com/ishidawataru/xcvr-emu/commit/ef1c59d34fac54b767b5335eaac8ae90fcb56567))

## [1.1.0](https://github.com/ishidawataru/xcvr-emu/compare/v1.0.1...v1.1.0) (2024-12-20)


### Features

* add FileName to the field metadata ([095101b](https://github.com/ishidawataru/xcvr-emu/commit/095101bd745c38bb1e13e27376ce51b6760654f6))
* add SFF identifier values ([fbe5a40](https://github.com/ishidawataru/xcvr-emu/commit/fbe5a409c0eac5afaf4ee3060ec998b366aa9c7d))
* fix order of the generated fields ([74e551d](https://github.com/ishidawataru/xcvr-emu/commit/74e551d3a4665ef551722f00bf9e5e29655a54db))
* support passing intial config to the server ([df538af](https://github.com/ishidawataru/xcvr-emu/commit/df538af5af5d043b12a5d42b27ecd543f8750180))


### Bug Fixes

* add missing EnumClass ([27459d6](https://github.com/ishidawataru/xcvr-emu/commit/27459d6b510c83d105068567b5a70fb85cce476b))
* fix build ([ae73e3f](https://github.com/ishidawataru/xcvr-emu/commit/ae73e3f73ed59cc3dab1346d862cb189513beacb))
* fix DPSM state handling ([10a27fe](https://github.com/ishidawataru/xcvr-emu/commit/10a27fe79bbac722e1d3bf973dc0cccb42552923))
* fix missing dependency ([9091747](https://github.com/ishidawataru/xcvr-emu/commit/909174799c2b94f5a5dc79d087f5465d40d53c76))
* fix naming for reserved and custom entries ([b97f3c8](https://github.com/ishidawataru/xcvr-emu/commit/b97f3c890d5b9034edf40693d66e8170762a24a4))
* **gen:** fix bug of enumcls subclassing ([9b4323c](https://github.com/ishidawataru/xcvr-emu/commit/9b4323cf45856457fec173628f34f06120dfc3e1))


### Documentation

* update README and add usage documentation for xcvr-emush ([b5b6055](https://github.com/ishidawataru/xcvr-emu/commit/b5b60550965e02cba5dba431a2d3786336f0fdae))

## [1.0.1](https://github.com/ishidawataru/xcvr-emu/compare/v1.0.0...v1.0.1) (2024-12-12)


### Bug Fixes

* fix wrong cmis import ([b8dc3be](https://github.com/ishidawataru/xcvr-emu/commit/b8dc3bee9872b78908a775b2a10b4380c5535fc2))

## [1.0.0](https://github.com/ishidawataru/xcvr-emu/compare/v0.2.0...v1.0.0) (2024-12-12)


### ⚠ BREAKING CHANGES

* migration to cmis library

### Features

* add main entry point to xcvr_emud and xcvr_emush scripts ([b101c21](https://github.com/ishidawataru/xcvr-emu/commit/b101c21210d1c8eb04d7b4bb75ac5619fbd62adc))
* **client:** Create/Delete support ([10c4c1e](https://github.com/ishidawataru/xcvr-emu/commit/10c4c1ebea9bad504079ba6800bc149253c51e0c))
* migration to cmis library ([601e211](https://github.com/ishidawataru/xcvr-emu/commit/601e2117e6ae40b617b8c586a4dd005451af0a7c))
* **server:** add type hint for Monitor method ([7f04ad8](https://github.com/ishidawataru/xcvr-emu/commit/7f04ad84bcfc7830aa0176f83ca9b02d8f8f23d8))
* **server:** refactor server management and improve shutdown handling ([a149972](https://github.com/ishidawataru/xcvr-emu/commit/a149972a30ce0725dbea0b531205d2dbe2a6a7fd))
* **transceiver:** add ModuleGlobalControls and update low power handling ([27eaff9](https://github.com/ishidawataru/xcvr-emu/commit/27eaff935b09e80608e667e1bc47c71e83ebb1ee))

## [0.2.0](https://github.com/ishidawataru/xcvr-emu/compare/v0.1.0...v0.2.0) (2024-11-17)


### Features

* add Create/Delete APIs ([a9026e3](https://github.com/ishidawataru/xcvr-emu/commit/a9026e3cd834a1d87189cfc76ef0d1338011fc59))
* **server:** implement Create/Delete APIs ([e9810cb](https://github.com/ishidawataru/xcvr-emu/commit/e9810cba27f245d4556fd73c1cc7daf5474a39a3))


### Bug Fixes

* add type annotations to EmulatorServer ([f7f5213](https://github.com/ishidawataru/xcvr-emu/commit/f7f5213bf8b82da1f02029fb98035a1a3336650e))

## 0.1.0 (2024-11-17)


### Bug Fixes

* **ci:** build image ([8ca8a89](https://github.com/ishidawataru/xcvr-emu/commit/8ca8a8987686b308eb244990cec20979c6d45c1e))
