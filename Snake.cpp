// Snake.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include<SFML/Graphics.hpp>
#include<time.h>
int main()
{
	sf::Texture blockTexture;
	sf::Vector2<int>fieldsize(45, 20);
	if (!blockTexture.loadFromFile("D:\\mini_project\\material\\block.png"))
	{
		std::cout << "block.png is not found." << std::endl;
		return EXIT_FAILURE;
	}
	sf::Sprite block(blockTexture);
	sf::Vector2<int>head(10, 6);
	std::vector < sf::Vector2<int>>snake = { head };
	srand(unsigned int(time(NULL) + rand()));
	sf::Vector2<int>food(rand() % fieldsize.x, rand() % fieldsize.y);
	//std::cout << food.x << std::endl;
	//std::cout << food.y << std::endl;
	sf::Vector2<float>blocksize(block.getLocalBounds().width, block.getLocalBounds().height);
	sf::RenderWindow window(sf::VideoMode(unsigned int(fieldsize.x * blocksize.x), unsigned int(fieldsize.y * blocksize.y)), L"貪食蛇");
	//留意型別轉換C2440
	enum class CDirection
	{
		up, down, left, right
	};
	CDirection direction = CDirection::right;
	sf::Clock clock;
	bool isdead = false;
	int sum = 0;
	while (window.isOpen())
	{
		//偵測處理使用者互動
		sf::Event event;
		if (window.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
			{
				window.close();
			}

		}
		if (event.type == sf::Event::KeyPressed)
		{
			if (event.key.code == sf::Keyboard::Up)
			{
				direction = CDirection::up;
			}
			if (event.key.code == sf::Keyboard::Down)
			{
				direction = CDirection::down;
			}
			if (event.key.code == sf::Keyboard::Left)
			{
				direction = CDirection::left;
			}
			if (event.key.code == sf::Keyboard::Right)
			{
				direction = CDirection::right;
			}
		}
		//物體移動
		if (clock.getElapsedTime().asSeconds() >= 0.5f)
		{
			sf::Vector2<int>head = snake[0];
			if (direction == CDirection::up)
			{
				head.y = head.y - 1;
			}
			if (direction == CDirection::down)
			{
				head.y = head.y + 1;
			}
			if (direction == CDirection::left)
			{
				head.x = head.x - 1;
			}
			if (direction == CDirection::right)
			{
				head.x = head.x + 1;
			}
			if (head.x < 0 || head.x >= fieldsize.x || head.y < 0 || head.y >= fieldsize.y)
			{
				isdead = true;

			}
			//是否吃到食物?
			if (!isdead) {
				if (food == head)
				{
					food.x = rand() % fieldsize.x;
					food.y = rand() % fieldsize.y;
					//std::cout << food.x << std::endl;
					//std::cout << food.y << std::endl;
					sum = sum + 1;
					std::cout << "吃了第" << sum << "個食物" << std::endl;
				}
				else
				{
					snake.pop_back();
				}
				snake.insert(snake.begin(), head);
			}
			clock.restart();
		}
		if (isdead)
		{
			window.clear(sf::Color(255, 0, 0));
			if (event.type == sf::Event::KeyPressed)
			{
				isdead = false;
				sum = 0;
				snake = { head };
			}
		}
		else
		{
			window.clear();
		}

		//繪製蛇
		for (const sf::Vector2<int>& body : snake) {
			sf::Vector2<float>bodyposition(body.x * blocksize.x, body.y * blocksize.y);
			block.setPosition(bodyposition);//函式多載
			window.draw(block);
		}

		//繪製食物
		sf::Vector2<float>foodposition(food.x * blocksize.x, food.y * blocksize.y);
		block.setPosition(foodposition);
		window.draw(block);
		window.display();
	}
	return EXIT_SUCCESS;
}


// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
