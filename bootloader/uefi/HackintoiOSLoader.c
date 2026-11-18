#include <Uefi.h>

#include <Library/UefiLib.h>

STATIC
VOID
ShowMenu (
  VOID
  )
{
  Print(L"\r\n");
  Print(L"  HackintoiOS UEFI development loader\r\n");
  Print(L"  -----------------------------------\r\n");
  Print(L"  [1] About this prototype\r\n");
  Print(L"  [2] Moto G60 target status\r\n");
  Print(L"  [3] Firmware environment report\r\n");
  Print(L"  [Esc] Exit to UEFI firmware\r\n");
  Print(L"\r\n");
  Print(L"  Select an option using the UEFI console keyboard.\r\n");
}

STATIC
VOID
ShowFirmwareReport (
  VOID
  )
{
  Print(L"\r\n  UEFI environment report\r\n");
  Print(L"  -----------------------\r\n");
  Print(L"  Firmware vendor: %s\r\n", gST->FirmwareVendor);
  Print(L"  Firmware revision: 0x%08x\r\n", gST->FirmwareRevision);
  Print(L"  Configuration tables: %u\r\n", gST->NumberOfTableEntries);
  Print(L"  Console input: %s\r\n",
        (gST->ConIn != NULL) ? L"available" : L"unavailable");
  Print(L"  Console output: %s\r\n",
        (gST->ConOut != NULL) ? L"available" : L"unavailable");
  Print(L"  Boot services: %s\r\n",
        (gBS != NULL) ? L"available" : L"unavailable");
  Print(L"\r\n  This report describes the current firmware only.\r\n");
  Print(L"  It does not identify or validate Moto G60 hardware.\r\n");
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
  Print(L"       HackintoiOS - UEFI development\r\n");
  Print(L"  =========================================\r\n");
  Print(L"\r\n");
  Print(L"  Experimental AArch64 UEFI application.\r\n");
  Print(L"  QEMU development target; HANOIP support\r\n");
  Print(L"  and Moto G60 firmware compatibility are\r\n");
  Print(L"  not yet implemented or verified.\r\n");

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
        Print(L"\r\n  HackintoiOS loader prototype v0.2\r\n");
        Print(L"  AArch64 UEFI application built with EDK II.\r\n");
        Print(L"  No kernel is loaded and no handoff is attempted.\r\n");
        break;

      case L'2':
        Print(L"\r\n  Target: Motorola Moto G60 Vision (XT2135-2)\r\n");
        Print(L"  Device family: HANOIP\r\n");
        Print(L"  Native UEFI availability: NOT VERIFIED\r\n");
        Print(L"  Device-specific boot integration: NOT IMPLEMENTED\r\n");
        break;

      case L'3':
        ShowFirmwareReport();
        break;

      case 0x1B:
        Print(L"\r\n  Returning from the prototype application.\r\n");
        return EFI_SUCCESS;

      default:
        Print(L"\r\n  Unknown key. Choose 1, 2, 3, or Esc.\r\n");
        break;
    }

    ShowMenu();
  }
}
