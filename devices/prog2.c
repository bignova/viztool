#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>
#include "cJSON.h" 
#include "randomrange.h"
#include <time.h>
#include <sys/types.h>
//combined the craft and client functions of origional demo
int client_combined(char *row, char *variable, int value, char *ip, int port){
	
	struct sockaddr_in address;
    int sock = 0, valread;
    struct sockaddr_in serv_addr;
    char buffer[1024] = {0};
//creates the socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }
  
    memset(&serv_addr, '0', sizeof(serv_addr));
  
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port);
      
    // Convert IPv4 and IPv6 addresses from text to binary form
    if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)<=0) 
    {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }
//connects to the socket
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
        return -1;
    }
	
	
	char src[] = "_update";
	int n = (sizeof(variable)+8);
	char cevent[n];
	strcpy(cevent, variable);
	strcat(cevent, src);

	char color[7];
	if (value == 10) {
		strcpy(color, "aqua");
	}else if (value >= 9){
		strcpy(color, "green");
	}else if (value >= 8){
		strcpy(color, "yellow");
	}else if (value >= 7){
		strcpy(color, "orange");
	}else if (value == 0){
		strcpy(color, "white");
	}else{
		strcpy(color, "red");
	}
	//char *out;
	cJSON *root, *header, *data, *urlExt, *url, *device, *event;
	cJSON *jrow, *jcolumn, *jvalue, *jcolor;
	
	root = cJSON_CreateObject();
	header = cJSON_CreateObject();
	data = cJSON_CreateObject();
	
	urlExt = cJSON_CreateArray();
	url = cJSON_CreateString("scoreboard");
	cJSON_AddItemToArray(urlExt,url);
	cJSON_AddItemToObject(header, "urlExtension", urlExt);
	
	device = cJSON_CreateString("prog1");
	cJSON_AddItemToObject(header, "device", device);
	event = cJSON_CreateString(cevent);
	cJSON_AddItemToObject(header, "event", event);
	
	jrow = cJSON_CreateString(row);
	cJSON_AddItemToObject(data, "row", jrow);
	jcolumn = cJSON_CreateString(variable);
	cJSON_AddItemToObject(data, "column", jcolumn);
	if(value == 0){
		jvalue = cJSON_CreateString("prog2.c");
	}else{
		jvalue = cJSON_CreateNumber(value);
	}
	cJSON_AddItemToObject(data, "value", jvalue);
	jcolor = cJSON_CreateString(color);
	cJSON_AddItemToObject(data, "color", jcolor);
	
	cJSON_AddItemToObject(root, "header", header);
	cJSON_AddItemToObject(root, "data", data);
	
//creates a string out of the json to be sent to hub
	char *returnme = cJSON_Print(root);
	send(sock,returnme,strlen(returnme), 0);
	valread = read( sock , buffer, 1024);
    printf("%s\n",buffer );
}



int main(){
	while(1) {
		char HOST[] = "localhost";
		int PORT = 4545;
		int the_num = randomrange(1,3);
		char var[2];
		if (the_num == 1){
			strcpy(var, "x");
		} else if(the_num == 2){
			strcpy(var, "y");
		} else {
			strcpy(var, "z");
		}
		int new_val = randomrange(1,10);
		
		client_combined("Current Value", var, new_val, HOST, PORT);
		client_combined("Last Update From", var, 0, HOST, PORT);
		sleep(2);
		printf("end");
	}
	return 1;
}