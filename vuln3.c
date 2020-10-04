#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int game(int);
//int jackpot();
void foo(char *);


/* nobody wins THIS time!!!
int jackpot() {
	printf("You just won!\n");
	printf("Congratulations!\n");
	return 0;
}*/

int game(int user_pick) {
	int rand_pick;

	if ((user_pick < 1) || (user_pick > 32000)) {
		printf("You must pick a value from 1- 32000\n");
		printf("Use help or -h for help\n");
		return 0;
	}

	printf("Playing the game of chance..\n");
	rand_pick = (rand() % 32000) + 1;
	printf("You picked: %d\n", user_pick);
	printf("Random value: %d\n", rand_pick);
	
	//if (user_pick == rand_pick)
		//jackpot();
	//else
		printf("Sorry, you didn't win this time...\n");
}


void foo(char* input) {
	char buffer[512];
	srand(time(NULL));
	strcpy(buffer, input);

	if ((!strcmp(buffer, "help")) || (!strcmp(buffer, "-h"))) {
		printf("Help Text:\n\n");
		printf("This is a game of chance.\n");
		printf("To play, simply guess a number 1 through 32000\n");
		printf("If you guess the number I am thinking of you win\n");
	}
	else
	{
		printf("buffer is at %p\n", &buffer);
		game(atoi(buffer));
	}
}


int main(int argc, char* argv[])
{
	if (argc < 2) {
		printf("Usage %s <a number 1 - 32000>\n", argv[0]);
		printf("use %s help or %s -h for more help.\n", argv[0], argv[0]);
		exit(0);
	}
	foo(argv[1]);
	printf("finished program!\n");
	return 0;
}