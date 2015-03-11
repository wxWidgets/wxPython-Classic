/**
 * Compile with Visual C++ or with:
 *  mingw32-gcc -Wall -Wl,--subsystem,windows -DUNICODE recycle.c -o recycle.exe
 *
 * Delete the given file or directory (an absolute path passed as argv[1]).
 * Returns 1 if the argument is invalid, or SHFileOperation return value
 * (0 if successful, nonzero otherwise)
 *
 * Author: Rudi Pettazzi
 */

#include <windows.h>

/* disable deprecated warning for wcscpy if compiled with Visual C++ */
#pragma warning(disable : 4996)

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
                    LPSTR lpCmdLine, int nCmdShow)
{
    wchar_t filename[MAX_PATH + 1] = { 0 };
    SHFILEOPSTRUCT sfo;
    size_t len = 0;
    int wargc = 0;
    int ret = 0;
    wchar_t **wargv = CommandLineToArgvW(GetCommandLineW(), &wargc);

    if (wargv == 0 || wargc < 2)
      return 1;

    len = wcslen(wargv[1]);

    if (len >= MAX_PATH)
        return 1;

    wcscpy(filename, wargv[1]);
    wcscpy(filename + wcslen(filename) + 1, L"\0");

    ZeroMemory(&sfo, sizeof(sfo));

    sfo.hwnd = NULL;
    sfo.wFunc = FO_DELETE;
    sfo.pFrom = filename;

    /* XXX FOF_NOERRORUI should be off to enable native error messages */
    sfo.fFlags = FOF_SILENT | FOF_NOERRORUI | FOF_ALLOWUNDO
                | FOF_NOCONFIRMMKDIR | FOF_NOCONFIRMATION;

    /* 0 if successful, nonzero otherwise. */
    ret = SHFileOperation(&sfo);

    LocalFree(wargv);

    return ret;
}


//
// Command-line utility to send a file or directory to the Recycle Bin
//
// This program only looks at the first command-line argument.
// That argument must be a full path to the file.
//

/*#include <windows.h>*/
/*#include <string.h>*/

/*int main( int argc, char *argv[] )*/
/*{*/
/*	char filename[2048] = {0};*/
/*    SHFILEOPSTRUCT sfo = {0};*/

/*    if ( !argc ) return( 0 );*/
/*    if ( strlen(argv[1]) > 2048 ) return( 0 );*/

/*	sfo.hwnd = NULL;*/
/*	sfo.wFunc = FO_DELETE;*/
/*	sfo.pFrom = filename;*/
/*	sfo.fFlags = FOF_SILENT | FOF_NOCONFIRMATION | FOF_NOERRORUI | */
/*                 FOF_ALLOWUNDO | FOF_NOCONFIRMMKDIR;*/

/*    strcpy( filename, argv[1] );*/
/*    strcpy( filename + strlen(argv[1]), "\0\0" );*/

/*	return( SHFileOperation(&sfo) );*/
/*}*/
