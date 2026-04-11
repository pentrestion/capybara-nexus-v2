#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * A subtle heap-based buffer overflow that standard static analysis often misses.
 * The vulnerability is triggered only if the user-supplied size is calculated 
 * in a way that doesn't account for the null terminator after a specific logic branch.
 */
void vulnerable_process(char *input, int length) {
    // Standard tools look for fixed-size buffers.
    // Dynamic size allocation based on input.
    char *buffer = (char *)malloc(length);
    if (!buffer) return;

    // Logic error: If 'length' is exactly the size of 'input',
    // the following strcpy will overflow because 'length' didn't include +1.
    memcpy(buffer, input, length); 
    
    // Some complex logic here...
    printf("Processed input: %s\n", buffer); // UAF or OOB Read possible if buffer not null-terminated
    free(buffer);
}

int main() {
    char *malicious = "A" * 64;
    vulnerable_process(malicious, 64);
    return 0;
}
