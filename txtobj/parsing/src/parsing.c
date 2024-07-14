#include<stdio.h>
#include <stdlib.h>
#include <string.h>

#define CHUNK_SIZE 1024
#define N_BOUNDS 100

typedef struct {
    long start;
    long end;
} Bounds;

typedef struct {
    Bounds* bounds;
    int size;
    int capacity;
} BoundsList;


void BoundsList_new(BoundsList** ptr, int capacity) {
    Bounds* head = malloc(sizeof(Bounds) * capacity);
    BoundsList* lst = malloc(sizeof(BoundsList));
    lst->bounds=head;
    lst->capacity=capacity;
    lst->size=0;
    *ptr=lst;
}

void BoundsList_realloc(BoundsList** ptr) {
    BoundsList* bounds = *ptr;
    BoundsList* lst;
    BoundsList_new(&lst, bounds->capacity * 2);
    Bounds* p = bounds->bounds;
    for (int i = 0; i < bounds->size; i++) {
        lst->bounds[i] = *p;
        p++;
        lst->size++;
    }
    free(bounds->bounds);
    free(bounds);
    *ptr = lst;
}

void BoundsList_add(BoundsList** ptr, Bounds item) {
    if ((*ptr)->size == (*ptr)->capacity) {
        BoundsList_realloc(ptr);
    }
    (*ptr)->bounds[(*ptr)->size] = item;
    (*ptr)->size++;
}



BoundsList get_bounds(
    char* path, 
    char* start_token, 
    int start_token_size, 
    char* end_token, 
    int end_token_size
) {
    FILE* f = fopen(path, "r");
    BoundsList* lst;
    BoundsList_new(&lst, 2);

    char* buffer = (char*) malloc(CHUNK_SIZE);

    int start_matches_end = strcmp(start_token, end_token);
    // indexes into the start/end token strings
    int start_i = 0, end_i = 0;
    // start token found when outside of a block --> mark block, increment depth
    // start token found when inside of block --> increment depth
    // end token found when outside of block --> ignore, should not have end token before start
    //                                     (if we do it is likely by accident)
    // end token found when inside of block --> decrement depth, if depth is 0 then mark end of block
    int depth = 0, in_block = 0;
    long block_start, block_end;
    long offset = ftell(f);
    int n_read;
    char c;
    while(1) {
        n_read = fread(buffer, sizeof(char), CHUNK_SIZE, f);
        for (int i = 0; i < n_read; i++) {
            offset++;
            c = buffer[i];
            // check for end token if we are in a block
            // If we are not in a block yet, we can ignore end tokens
            if (in_block && c == end_token[end_i]) {
                end_i++;
                if (end_i == end_token_size) {
                    end_i = 0;
                    depth--;
                    if (depth == 0) {
                        in_block = 0;
                        block_end = offset - end_token_size;

                        // If the start and end tokens are different, then
                        // finding an end token implies this byte does not end a start token
                        // If they are the same, we should still treat it as an end token
                        // as we only get here if we are already inside of a block
                        Bounds b = {block_start, block_end};
                        BoundsList_add(&lst, b);
                        block_start = 0;
                        block_end = 0;

                        continue;
                    }
                }  
            } else {
                end_i = 0;
            }

            if (c == start_token[start_i]) {
                start_i++;
                if (start_i == start_token_size) {
                    // found a start token
                    start_i = 0;
                    block_start = offset;
                    if (in_block == 0) {
                        in_block = 1; 
                    }
                    depth += 1;
                }
            } else {
                // start searching again by the first charater in the token
                start_i = 0;
            }
        }
        if (n_read < CHUNK_SIZE) break;
    }

    free(buffer);
    fclose(f);
    return *lst;
}


void free_bounds(BoundsList bounds_list) {
    free(bounds_list.bounds);
}