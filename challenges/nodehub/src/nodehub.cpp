#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include "personalize.h"

/*
===============================================================================
LINUX SPECIFIC HEADERS
===============================================================================
*/

extern "C" {
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/utsname.h>
#include <unistd.h>
}

/*
===============================================================================
MACRO DEFINITIONS
===============================================================================
*/

#define PRINT(s) write(1, s, strlen(s));
#define PRINT_ERR(s) write(2, s, strlen(s));

/*
===============================================================================
FORWARD DECLARATIONS
===============================================================================
*/

static void print_num(size_t);
static void vault_add_token(size_t);
static void vault_del_token(size_t);
static void vault_crypt(size_t, char *, size_t);
class SensorNode;

struct Token {
    size_t len;
    char token[24];
};

/*
===============================================================================
CONSTANT DEFINITIONS
===============================================================================
*/

static const size_t MAX_CMD = 25;
static const size_t MAX_NODES = 20;
static const size_t MAX_DESC = 4096;
static const size_t MAX_TAG = 24;
static const size_t MAX_FLAG = 40;
static const size_t MAX_IP = 46;
static const size_t MAX_TOKENS = 10;

/*
===============================================================================
GLOBAL STATE
===============================================================================
*/

static char desc_buff[MAX_DESC];
static Token tokens[MAX_TOKENS];
static SensorNode *node_list[MAX_NODES];


/*
===============================================================================
CLASS DEFINITIONS
===============================================================================
*/

class SensorNode {
public:
    char *desc;
    uint32_t desc_len;
    uint32_t desc_allocated;
    char ip[MAX_IP + 2];
    uint32_t padding;
    uint16_t desc_version;
    uint16_t port;
    char tag[MAX_TAG];

    SensorNode() {
        this->desc = nullptr;
        this->desc_len = 0;
        this->desc_allocated = 0;
        this->desc_version = 0;
        this->port = 0;
        this->padding = 0;
        memset(&this->ip, 0, MAX_IP + 2);
        memset(&this->tag, 0, MAX_TAG);
    }

    virtual ~SensorNode() {
        free_desc();

        this->desc = nullptr;
        this->desc_len = 0;
        this->desc_allocated = 0;
    }

    virtual void update_desc(size_t len, uint16_t version, char *description) {
        if (!description)
            return;
        
        this->desc = description;
        this->desc_len = len;
        this->desc_version = version;
        this->desc_allocated = 1;
    }

    void free_desc() {
        char *desc = this->desc;
        if (!desc) {
            this->desc_allocated = 0;
            return;
        }

        if (this->desc_allocated) {
            memset(desc, 0, this->desc_len);
            delete[] desc;
            this->desc_allocated = 0;
        }
    }

    virtual void print_desc() {
        PRINT("Version: ");
        print_num(this->desc_version);
        PRINT("\n");
    }
};

class AuthenticatedNode : public SensorNode {
private:
    size_t auth_id;

public:
    AuthenticatedNode(size_t auth_id) : SensorNode(), auth_id(auth_id) { }

    ~AuthenticatedNode() {
        vault_del_token(this->auth_id);
    }

    virtual void update_desc(size_t len, uint16_t version, char *description) {
        SensorNode::update_desc(len, version, description);

        if (!description)
            return;

        vault_crypt(this->auth_id, description, len);
    }

    virtual void print_desc() {
        SensorNode::print_desc();

        if (this->desc) {
            /* Decrypt description */
            vault_crypt(this->auth_id, this->desc, this->desc_len);

            PRINT("Description: ");
            write(1, this->desc, this->desc_len);
            PRINT("\n");

            /* Encrypt description again */
            vault_crypt(this->auth_id, this->desc, this->desc_len);
        }
    }
};

class UnauthenticatedNode : public SensorNode {
public:
    UnauthenticatedNode() : SensorNode() { }

    virtual void update_desc(size_t len, uint16_t version, char *description) {
        SensorNode::update_desc(len, version, description);
    }

    virtual void print_desc() {
        SensorNode::print_desc();

        if (this->desc) {
            PRINT("Description: ");
            write(1, this->desc, this->desc_len);
            PRINT("\n");
        }
    }
};

/*
===============================================================================
FUNCTION DEFINITIONS
===============================================================================
*/

[[ noreturn ]] static void bail_out() {
    PRINT_ERR("Exiting...\n");
    _exit(EXIT_FAILURE);
}

[[ noreturn ]] static void quit() {
    PRINT("Bye!\n");
    _exit(EXIT_SUCCESS);
}

static void print_uname() {
    utsname buf;

    memset(&buf, 0, sizeof(utsname));
    if (uname(&buf)) {
        PRINT_ERR("Erropr during uname.\n");
        bail_out();
    }
    
    write(1, buf.sysname, strlen(buf.sysname));
    write(1, " ", 1);
    write(1, buf.nodename, strlen(buf.nodename));
    write(1, " ", 1);
    write(1, buf.release, strlen(buf.release));
    write(1, " ", 1);
    write(1, buf.version, strlen(buf.version));
    write(1, " ", 1);
    write(1, buf.machine, strlen(buf.machine));
    write(1, "\n", 1);
}

static size_t read_line(char *buffer, size_t max_length) {
    size_t i;
    char c;

    for (i = 0; i < max_length; i++) {
        if (read(0, &c, 1) != 1)
            break;
        if (c == '\n')
            break;

        buffer[i] = c;
    }

    return i;
}

static void print_num(size_t n) {
    char num_buffer[30];
    int counter;

    memset(num_buffer, 0, 30);
    counter = snprintf(num_buffer, 30, "%ld", n);
    write(1, num_buffer, counter);
}

static bool read_num(ssize_t *n) {
    char buf[30];

    memset(buf, 0, 30);
    if (!read_line(buf, 29))
        return false;

    *n = strtoll(buf, nullptr, 0);
    return true;
}

static ssize_t select_node() {
    ssize_t node;

    PRINT("Node-ID: ");
    if (!read_num(&node)) {
        PRINT("Invalid input.\n");
        return -1;
    }

    if (node < 0 || (size_t)node >= MAX_NODES) {
        PRINT("Invalid input.\n");
        return -1;
    }

    return node;
}

static uint16_t read_version() {
    ssize_t version;

    PRINT("Version: ");
    if (!read_num(&version)) {
        PRINT("Invalid version, defaulting to 1.\n");
        return 1;
    }

    if (version < 0 || version >= 65536){
        PRINT("Invalid version, defaulting to 1.\n");
        return 1;
    }

    return (uint16_t)version;
}

static void read_description(char *desc, size_t *len, uint16_t *version) {
    size_t i;
    size_t counter;

    *version = read_version();

    PRINT("Enter description (send empty line to finish):\n")
    memset(desc, 0, MAX_DESC);

    /* Allow sending multiple lines of input for the description */
    for (i = 0; i < MAX_DESC; ) {
        counter = read_line(&desc[i], MAX_DESC - i);
        if (!counter)
            break;

        i += counter; 

        if (i < MAX_DESC) {
            desc_buff[i] = '\n';
            i += 1;
        }
    }

    counter = i;
    if (counter >= MAX_DESC)
        counter = MAX_DESC - 1;
    desc[counter] = '\0';
    *len = counter;
}


static void vault_add_token(size_t id) {
    if (id >= MAX_TOKENS) {
        PRINT_ERR("Invalid token ID.\n");
        bail_out();
    }

    PRINT("Auth-Token: ");
    tokens[id].len = read_line(tokens[id].token, sizeof(tokens[id].token));
}

static void vault_del_token(size_t id) {
    if (id >= MAX_TOKENS) {
        PRINT_ERR("Invalid token ID.\n");
        bail_out();
    }

    memset(&tokens[id], 0, sizeof(tokens));
}

static void vault_crypt(size_t id, char *desc, size_t desc_len) {
    size_t i, token_len;

    if (id >= MAX_TOKENS) {
        PRINT_ERR("Invalid token ID.\n");
        bail_out();
    }

    if (tokens[id].len == 0) {
        PRINT_ERR("Token not initialized.\n");
        bail_out();
    }

    token_len = tokens[id].len;
    for (i = 0; i < desc_len; i++)
        desc[i] ^= tokens[id].token[i % token_len];
}

void vault_flag() {
    int fd;
    ssize_t bytes_read;

    fd = open("./flg1", O_RDONLY);
    if (fd < 0) {
        PRINT_ERR("Could not open flag file");
        bail_out();
    }

    memset(desc_buff, 0, MAX_DESC);
    bytes_read = read(fd, desc_buff, MAX_DESC);
    if (bytes_read <= 0) {
        PRINT_ERR("Could not read flag.\n");
        bail_out();
    }

    PRINT("Flag: ");
    write(1, desc_buff, bytes_read);
    PRINT("\n");

    memset(desc_buff, 0, MAX_DESC);
    close(fd);
}

static void node_listing() {
    size_t i;

    for (i = 0; i < MAX_NODES; i++) {
        if (!node_list[i])
            continue;

        /* Print node ID */
        print_num(i);
        PRINT(": ");

        /* Print node tag */
        write(1, node_list[i]->tag, strlen(node_list[i]->tag));

        PRINT("\n");
    }
}

static void node_add(bool is_authenticated) {
    size_t i;
    size_t desc_len;
    size_t tag_len;
    ssize_t port;
    uint16_t desc_version;
    char *desc_chunk;
    SensorNode *current_node;
    char cmd_buff[MAX_CMD];

    for (i = 0; i < MAX_NODES; i++) {
        if (!node_list[i])
            break;
    }

    if (i == MAX_NODES) {
        PRINT("Cannot add more nodes.\n");
        return;
    }

    if (is_authenticated) {
        PRINT("Adding new authenticated node with ID ");
        print_num(i);
        PRINT(".\n");

        current_node = new AuthenticatedNode(i);

        /* Add authentication token to the ID */
        vault_add_token(i);
    } else {
        PRINT("Adding new unauthenticated node with ID ");
        print_num(i);
        PRINT(".\n");

        current_node = new UnauthenticatedNode();
    }

    /* Make user enter a node tag for identification */
    PRINT("Node-Tag: ");
    tag_len = read_line(cmd_buff, MAX_CMD);
    if (strlen(cmd_buff) >= MAX_TAG) {
        PRINT("Tag too long, cutting it off.\n");
        tag_len = MAX_TAG;
        cmd_buff[MAX_TAG - 1] = '\0';
    }
    memcpy(current_node->tag, cmd_buff, tag_len);

    /* Read endpoint information */
    PRINT("IP: ");
    read_line(current_node->ip, 46);
    PRINT("Port: ");
    port = 0;
    read_num(&port);
    current_node->port = (uint16_t)port;

    /* Make user enter a description for the sensor node */
    read_description(desc_buff, &desc_len, &desc_version);
    if (desc_len > 0) {
        desc_chunk = new char [desc_len];
        memcpy(desc_chunk, desc_buff, desc_len);
    } else {
        desc_chunk = nullptr;
    }
    current_node->update_desc(desc_len, desc_version, desc_chunk);

    node_list[i] = current_node;
}

static void node_del() {
    ssize_t n;
    SensorNode *current_node;

    n = select_node();
    if (n < 0)
        return;
    current_node = node_list[n];
    if (!current_node)
        return;
    
    delete current_node;
    node_list[n] = nullptr;
}

static void node_print_desc() {
    ssize_t n;
    SensorNode *current_node;

    n = select_node();
    if (n < 0)
        return;
    current_node = node_list[n];
    if (!current_node)
        return;

    current_node->print_desc();
}

static void node_update_desc() {
    ssize_t n;
    SensorNode *current_node;
    size_t desc_len;
    uint16_t desc_version;
    char *desc_chunk;

    n = select_node();
    if (n < 0)
        return;
    current_node = node_list[n];
    if (!current_node)
        return;

    read_description(desc_buff, &desc_len, &desc_version);
    if (desc_len > 0) {
        desc_chunk = new char [desc_len];
        memcpy(desc_chunk, desc_buff, desc_len);
    } else {
        desc_chunk = nullptr;
    }
    current_node->free_desc();
    current_node->update_desc(desc_len, desc_version, desc_chunk);
}

static int cmd_loop_main() {
    char cmd_buff[MAX_CMD];

    while (true) {
        PRINT("#> ");

        memset(cmd_buff, 0, MAX_CMD);
        if (!read_line(cmd_buff, MAX_CMD)) {
            PRINT_ERR("Read empty command.\n");
            bail_out();
        }

        if (!strncmp(cmd_buff, "help", MAX_CMD)) {
            PRINT("Available commands:\n\n");
            PRINT("nodes\n");
            PRINT("uname\n");
            PRINT("quit\n");
        } else if (!strncmp(cmd_buff, "nodes", MAX_CMD)) {
            return 1;
        } else if (!strncmp(cmd_buff, "uname", MAX_CMD)) {
            print_uname();
        } else if (!strncmp(cmd_buff, "quit", MAX_CMD)) {
            quit();
        } else {
            PRINT("Unknown command.\n");
        }
    }
}

static int cmd_loop_nodes() {
    char cmd_buff[MAX_CMD];

    while (true) {
        PRINT("nodes> ");

        memset(cmd_buff, 0, MAX_CMD);
        if (!read_line(cmd_buff, MAX_CMD))
            return 1;

        if (!strncmp(cmd_buff, "help", MAX_CMD)) {
            PRINT("Available commands:\n\n");
            PRINT("list\n");
            PRINT("add\n");
            PRINT("add_auth\n");
            PRINT("del\n");
            PRINT("update_desc\n");
            PRINT("print_desc\n");
            PRINT("quit\n");
        } else if (!strncmp(cmd_buff, "list", MAX_CMD)) {
            node_listing();
        } else if (!strncmp(cmd_buff, "add", MAX_CMD)) {
            node_add(false);
        } else if (!strncmp(cmd_buff, "add_auth", MAX_CMD)) {
            node_add(true);
        } else if (!strncmp(cmd_buff, "del", MAX_CMD)) {
            node_del();
        } else if (!strncmp(cmd_buff, "update_desc", MAX_CMD)) {
            node_update_desc();
        } else if (!strncmp(cmd_buff, "print_desc", MAX_CMD)) {
            node_print_desc();
        } else if (!strncmp(cmd_buff, "quit", MAX_CMD)) {
            return 0;
        } else {
            PRINT("Unknown command.\n");
        }
    }
}

/*
===============================================================================
MAIN PROGRAM 
===============================================================================
*/
int main() {
    int state;

    personalize_heap_layout();

    /* Initialization */

    state = 0;
    memset(node_list, 0, MAX_NODES * sizeof(SensorNode *));

    /* Program header and start of user interaction */

    PRINT(R"(      ___          ___          ___          ___          ___          ___          ___     )" "\n");
    PRINT(R"(     /\__\        /\  \        /\  \        /\  \        /\__\        /\__\        /\  \    )" "\n"); 
    PRINT(R"(    /::|  |      /::\  \      /::\  \      /::\  \      /:/  /       /:/  /       /::\  \   )" "\n"); 
    PRINT(R"(   /:|:|  |     /:/\:\  \    /:/\:\  \    /:/\:\  \    /:/__/       /:/  /       /:/\:\  \  )" "\n"); 
    PRINT(R"(  /:/|:|  |__  /:/  \:\  \  /:/  \:\__\  /::\~\:\  \  /::\  \ ___  /:/  /  ___  /::\~\:\__\ )" "\n"); 
    PRINT(R"( /:/ |:| /\__\/:/__/ \:\__\/:/__/ \:|__|/:/\:\ \:\__\/:/\:\  /\__\/:/__/  /\__\/:/\:\ \:|__|)" "\n"); 
    PRINT(R"( \/__|:|/:/  /\:\  \ /:/  /\:\  \ /:/  /\:\~\:\ \/__/\/__\:\/:/  /\:\  \ /:/  /\:\~\:\/:/  /)" "\n"); 
    PRINT(R"(     |:/:/  /  \:\  /:/  /  \:\  /:/  /  \:\ \:\__\       \::/  /  \:\  /:/  /  \:\ \::/  / )" "\n"); 
    PRINT(R"(     |::/  /    \:\/:/  /    \:\/:/  /    \:\ \/__/       /:/  /    \:\/:/  /    \:\/:/  /  )" "\n"); 
    PRINT(R"(     /:/  /      \::/  /      \::/__/      \:\__\        /:/  /      \::/  /      \::/__/   )" "\n"); 
    PRINT(R"(     \/__/        \/__/        ~~           \/__/        \/__/        \/__/        ~~       )" "\n"); 
    PRINT("\n\n");

    PRINT("  Nodehub Control Terminal\n");
    PRINT("  Enter 'help' to get an overview of existing commands.\n\n");

    while (true) {
        switch (state) {
        case 0:
            state = cmd_loop_main();
            break;
        case 1:
            state = cmd_loop_nodes();
            break;
        default:
            PRINT_ERR("Unknown state.\n");
            bail_out();
        }
    }

    return EXIT_SUCCESS;
}
