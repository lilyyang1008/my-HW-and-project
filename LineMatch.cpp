// LineMatch.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include<SFML/Graphics.hpp>
sf::Vector2<float>getpixelposition(const sf::Vector2<int>& position, const sf::Vector2<unsigned int>& blocksize)
{
    return sf::Vector2<float>(float(position.x * blocksize.x), float(position.y * blocksize.y));
}


int main()
{
    const int fieldwidth = 6;
    const int fieldheight = 10;
    bool field[fieldheight][fieldheight] = {};
    for (int y = 3; y < fieldheight; y++)
    {
        for (int i = 1; i <= 3; i++)
        {
            field[rand() % fieldwidth][y] = true;
        }
    }
    sf::Texture blocktexture;
    blocktexture.loadFromFile("D:\\mini_project\\material\\block.png");
    sf::Vector2<unsigned int>blocksize(blocktexture.getSize());
    const int windowwidth = blocksize.x * fieldwidth;
    const int windowheight = blocksize.y * fieldheight;
    sf::String title(L"簡易消行遊戲");
    sf::RenderWindow window(sf::VideoMode(windowwidth, windowheight), title);
    sf::Sprite block(blocktexture);
    sf::Vector2<int>originposition(fieldwidth / 2, 0);
    sf::Vector2<int>position(originposition);
    block.setPosition(getpixelposition(position, blocksize));
    //block.setPosition(float(position.x * blocksize.x), float(position.y * blocksize.y));
    sf::Clock clock;
    while (window.isOpen())
    {
        enum class Action
        {
            hold, moveleft, moveright, movedown,
        };
        Action action = Action::hold;
        sf::Event event;

        if (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
            {
                window.close();
            }
            if (event.type == sf::Event::KeyPressed)
            {
                if (event.key.code == sf::Keyboard::Left)
                {
                    action = Action::moveleft;//position.x = position.x - 1;
                }
                if (event.key.code == sf::Keyboard::Right)
                {
                    action = Action::moveright;//position.x = position.x + 1;
                }
                if (event.key.code == sf::Keyboard::Down)
                {
                    action = Action::movedown;//position.y = position.y + 1;
                }
            }
        }
        if (clock.getElapsedTime().asSeconds() >= 0.9)
        {
            action = Action::movedown;//position.y = position.y + 1;

            clock.restart();
        }
        sf::Vector2<int> nextposition = position;
        switch (action)
        {
        case Action::hold:
            break;
        case Action::movedown:
            nextposition.y = nextposition.y + 1;
            break;
        case Action::moveleft:
            nextposition.x = nextposition.x - 1;
            break;
        case Action::moveright:
            nextposition.x = nextposition.x + 1;
            break;
        default:
            break;
        }
        if (nextposition.x >= 0 && nextposition.x < fieldwidth && nextposition.y < fieldheight && field[nextposition.x][nextposition.y] == false)
        {
            position = nextposition;
        }
        else {
            if (action == Action::movedown)
            {
                field[position.x][position.y] = true;
                //檢查第position.y是否全滿
                bool isfull = true;
                for (int x = 0; x < fieldwidth; x++) {
                    if (field[x][position.y] == false)
                    {
                        isfull = false;
                    }
                }
                if (isfull)
                {
                    //position.y以上所有橫行往下移動一格
                    for (int y = position.y; y > 0; y--)
                    {
                        for (int x = 0; x < fieldwidth; x++)
                        {
                            field[x][y] = field[x][y - 1];
                        }
                    }
                    //消除最頂層
                    for (int x = 0; x < fieldwidth; x++)
                    {
                        field[x][0] = false;
                    }

                }

                position = originposition;
                
            }
        }

        window.clear();
        //block.setPosition(float(position.x * blocksize.x), float(position.y * blocksize.y));
        //控制的方塊
        block.setPosition(getpixelposition(position, blocksize));
        window.draw(block);
        //繪製到底部的方塊(場地)
        int x, y;
        for (x = 0; x < fieldwidth; x++)
        {
            for (y = 0; y < fieldheight; y++)
            {
                if (field[x][y] == true)
                {
                    sf::Vector2<int>position2(x, y);
                    block.setPosition(getpixelposition(position2, blocksize));
                    window.draw(block);
                }
            }
        }
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
