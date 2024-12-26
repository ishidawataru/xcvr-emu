import subprocess


def get_last_line(output):
    return output.stdout.decode().strip().split("\n")[-1].replace("\x00", "").strip()


def test_xcvr_emush():
    o = subprocess.run(
        ["xcvr-emush", "-c", "transceiver 0; read VendorName"],
        check=True,
        capture_output=True,
    )
    assert get_last_line(o) == "00h:129-144    | VendorName | xcvr-emu"

    o = subprocess.run(
        ["xcvr-emush", "-c", "transceiver 0; read ModuleState"],
        check=True,
        capture_output=True,
    )
    assert get_last_line(o) == "00h:3.1-3      | ModuleState | MODULE_LOW_PWR(1)"

    subprocess.run(
        ["xcvr-emush", "-c", "transceiver 0; write LowPwrRequestSW 0"],
        check=True,
    )

    o = subprocess.run(
        ["xcvr-emush", "-c", "transceiver 0; read ModuleState"],
        check=True,
        capture_output=True,
    )
    assert get_last_line(o) == "00h:3.1-3      | ModuleState | MODULE_READY(3)"
