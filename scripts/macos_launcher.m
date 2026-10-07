// Development runtime snapshot. No install, network or shell evaluation.
#import <AppKit/AppKit.h>
#include <unistd.h>
#include <stdlib.h>

static int fail(NSString *message) {
    [NSApplication sharedApplication];
    NSAlert *alert = [[NSAlert alloc] init];
    alert.messageText = @"AgentSafe";
    alert.informativeText = message;
    [alert runModal];
    return 1;
}

int main(void) {
    @autoreleasepool {
        NSString *root = @AGENTSAFE_RUNTIME;
        NSString *python = @AGENTSAFE_PYTHON;
        if (![[NSFileManager defaultManager] isExecutableFileAtPath:python]) {
            return fail(@"The development Python runtime is missing. Rebuild the launcher using the instructions in README.");
        }
        if (chdir(root.fileSystemRepresentation) || setenv("PYTHONPATH", root.fileSystemRepresentation, 1)) {
            return fail(@"The development runtime snapshot was removed. Rebuild the launcher using the instructions in README.");
        }
        const char *args[] = {python.fileSystemRepresentation, "-S", "-m", "agentsafe", "gui", "--lang", "zh", NULL};
        execv(args[0], (char *const *)args);
        return fail(@"AgentSafe could not start its local runtime. Check the development setup in README.");
    }
}
