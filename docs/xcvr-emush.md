# xcvr-emush

`xcvr-emush` is an interactive shell for `xcvr-emu`.
Once you start `xcvr-emud`, you can use `xcvr-emush` to interact with the emulator.

Here is the brief example of how to use `xcvr-emush`:

```bash
$ xcvr-emush
> create 0
> list
0: present: False
> transceiver 0
transceiver(0)> insert
transceiver(0)> info
Transceiver(0):
  present: True
  No DPSM configured
transceiver(0)> read ModuleState
Read: bank=0, page=0, offset=3, length=1, res.data=b'\x02'
00h:3.1-3      | ModuleState | MODULE_LOW_PWR(1)
transceiver(0)> read LowPwrRequestSW
Read: bank=0, page=0, offset=26, length=1, res.data=b'\x10'
00h:26.4       | LowPwrRequestSW | LOW_POWER_MODE(1)
transceiver(0)> write LowPwrRequestSW 0
transceiver(0)> read ModuleState
Read: bank=0, page=0, offset=3, length=1, res.data=b'\x06'
00h:3.1-3      | ModuleState | MODULE_READY(3)
transceiver(0)> info
Transceiver(0):
  present: True
  DPSM:
    DPID: 1, Active AppSel: 1, State: DPStateHostLaneEnum.DPINITIALIZED
transceiver(0)> remove
```

In the shell, you can use the following commands:

- `exit`: Exit `xcvr-emush`.
- `create <index>`: Create a transceiver with the specified index.
- `delete <index>`: Delete the transceiver with the specified index.
- `list`: List all transceivers.
- `transceiver <index>`: Select a transceiver to interact with.

Once you select a transceiver, the prompt will change to `transceiver(<index>)>` and you can use the following commands:

- `exit`: Exit `xcvr-emush`.
- `quit`: Go back to the main shell.
- `insert`: Emulate the insertion of a module.
- `remove`: Emulate the removal of a module.
- `info`: Show the information of the transceiver.
- `read <address>|<filed name>`: Read a register value.
- `write <address>|<filed name> <value>`: Write a register value.
- `reginfo <address>|<filed name>`: Show the description of the register.

The format of the address is `<page>h:<offset>.<bit>`. For example, `00h:3.1` means page 0, offset 3, bit 1.
offset and bit can be omitted. For example, `read 0h` will read the whole page 0. `read 0h:3` will read the page 0, offset 3.
In order to express multiple bytes or bits, you can use the following format: `read 0h:3-4` will read the page 0, offset 3 and 4. `read 0h:3.1-3` will read the page 0, offset 3, bit 1, 2, and 3.
