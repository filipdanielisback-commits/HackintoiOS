#include <Uefi.h>

#include <Library/UefiLib.h>

STATIC
VOID
ShowMenu (
  VOID
  )
{
  Print(L"\r\n");
  Print(L"  HackintoiOS UEFI loader prototype\r\n");
  Print(L"  ---------------------------------\r\n");
  Print(L"  [1] About this prototype\r\n");
  Print(L"  [2] Moto G60 device status\r\n");
  Print(L"  [Esc] Exit to UEFI firmware\r\n");
  Print(L"\r\n");
  Print(L"  Select an option using the UEFI console keyboard.\r\n");
}

EFI_STATUS
EFIAPI
UefiMain (
  IN EFI_HANDLE        ImageHandle,
  IN EFI_SYSTEM_TABLE  *SystemTable
  )
{
  EFI_STATUS     Status;
  EFI_INPUT_KEY  Key;
  UINTN          EventIndex;

  (VOID)ImageHandle;
  (VOID)SystemTable;

  gST->ConOut->ClearScreen(gST->ConOut);

  Print(L"\r\n");
  Print(L"  =========================================\r\n");
  Print(L"       HackintoiOS - UEFI loader prototype\r\n");
  Print(L"  =========================================\r\n");
  Print(L"\r\n");
  Print(L"  This is an experimental AArch64 UEFI app.\r\n");
  Print(L"  It is not a Moto G60 bootloader yet.\r\n");

  ShowMenu();

  for (;;) {
    Status = gBS->WaitForEvent(
                    1,
                    &gST->ConIn->WaitForKey,
                    &EventIndex
                    );
    if (EFI_ERROR(Status)) {
      Print(L"\r\n  Input wait failed: %r\r\n", Status);
      return Status;
    }

    Status = gST->ConIn->ReadKeyStroke(gST->ConIn, &Key);
    if (EFI_ERROR(Status)) {
      continue;
    }

    switch (Key.UnicodeChar) {
      case L'1':
        Print(L"\r\n  HackintoiOS loader prototype v0.1\r\n");
        Print(L"  Built as an AArch64 UEFI application with EDK II.\r\n");
        break;

      case L'2':
        Print(L"\r\n  Target: Motorola Moto G60 Vision (XT2135-2)\r\n");
        Print(L"  Platform family: HANOIP\r\n");
        Print(L"  UEFI availability on this phone: NOT VERIFIED\r\n");
        Print(L"  No device boot or hardware support is implemented.\r\n");
        break;

      case 0x1B:
        Print(L"\r\n  Returning from the prototype application.\r\n");
        return EFI_SUCCESS;

      default:
        Print(L"\r\n  Unknown key. Choose 1, 2, or Esc.\r\n");
        break;
    }

    ShowMenu();
  }
}
