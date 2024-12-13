# xcvr-emu <!-- omit in toc -->

`xcvr-emu` is a CMIS transceiver emulator.

## Table of Contents <!-- omit in toc -->
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

`xcvr-emu` is a [CMIS](https://www.oiforum.com/technical-work/hot-topics/management/) transceiver emulator. It is a software tool that emulates the behavior of a CMIS transceiver. It is intended to be used for testing and development purposes.

## Installation

To install `xcvr-emu`, you need to have Python 3.10 or later installed on your system. You can install `xcvr-emu` using `pip`:

```bash
pip install git+https://github.com/ishidawataru/xcvr-emu.git
```

Docker image is also available:

```bash
$ docker run -d --name xcvr-emu ghcr.io/ishidawataru/xcvr-emu
$ docker exec -it xcvr-emu xcvr-emush
> ?
quit, exit, list, create, delete, transceiver
>
```

## Usage

To start `xcvr-emu`, run the following command:

```bash
$ xcvr-emud
INFO:xcvr_emu.xcvr_emud:Server started at port 50051
```

You can use the following command to interact with the emulator:

```bash
$ xcvr-emush
quit, exit, list, create, delete, transceiver
>
```

For more information, please refer to the [./docs/xcvr-emush.md](./docs/xcvr-emush.md).

## License

`xcvr-emu` is licensed under the Apache License, Version 2.0. See [LICENSE](./LICENSE) for the full license text.
