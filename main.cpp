// tetrisgame.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <SFML/Graphics.hpp>

int main()
{
    const int fieldwidth = 10;
    const int fieldhight = 20;
    enum class type
    {
        None,o,i,L,
    };
    type field[fieldwidth][fieldhight] = {};
    sf::Texture backgroundtexture;
    if (!backgroundtexture.loadFromFile("background.png"))
    {
        return EXIT_FAILURE;
    }
    sf::Texture yellowTexture;
    if (!yellowTexture.loadFromFile("yellow.png"))
    {
        return EXIT_FAILURE;
    }
    sf::Texture lightbluetexture;
    if (!lightbluetexture.loadFromFile("light_blue.png"))
    {
        return EXIT_FAILURE;
    }
    sf::Texture greentexture;
    if (!greentexture.loadFromFile("green.png"))
    {
        return EXIT_FAILURE;
    }
    std::map<type,std::vector<std::vector<sf::Vector2<int>>>>shapes{
     { 
         type::o,
        {
         {sf::Vector2<int>(0,0),sf::Vector2<int>(1,0),sf::Vector2<int>(0,-1),sf::Vector2<int>(1,-1)}
        },
     },
     {
        type::i,
      {
      {sf::Vector2<int>(-1,0),sf::Vector2<int>(0,0),sf::Vector2<int>(1,0),sf::Vector2<int>(2,0)},
      {sf::Vector2<int>(0,-2),sf::Vector2<int>(0,-1),sf::Vector2<int>(0,0),sf::Vector2<int>(0,1)}
      }
     },
    {
        type::L,
        {
        {sf::Vector2<int>(0,2),sf::Vector2<int>(0,1),sf::Vector2<int>(0,0),sf::Vector2<int>(1,0)},
        {sf::Vector2<int>(0,-2),sf::Vector2<int>(0,-1),sf::Vector2<int>(0,0),sf::Vector2<int>(1,0)},
        {sf::Vector2<int>(0,-2),sf::Vector2<int>(0,-1),sf::Vector2<int>(0,0),sf::Vector2<int>(-1,0)},
        {sf::Vector2<int>(0,2),sf::Vector2<int>(0,1),sf::Vector2<int>(0,0),sf::Vector2<int>(-1,0)}
        }
    }
    };
    
    type currenttype=type(rand()%3+1);
    int currentindex = 0;
    //if (rand() % 2 == 0)
    {
        //currenttype = type::o;
    }
    //else
    {
        //currenttype = type::i;
    }
    const int blockwidth = yellowTexture.getSize().x;
    const int blockhight = yellowTexture.getSize().y;
    const int windowwidth = fieldwidth * blockwidth;
    const int windowheight = fieldhight * blockhight;
    std::map<type,sf::Sprite>sprites = {
        {type::o,sf::Sprite(yellowTexture)},
        {type::i,sf::Sprite(lightbluetexture)},
        {type::L,sf::Sprite(greentexture)},
    };
    backgroundtexture.setRepeated(true);
    sf::Sprite backgroundsprite(backgroundtexture,sf::IntRect(0,0,windowwidth,windowheight));
    std::vector<sf::Vector2<int>>currentshape;
    sf::Sprite currentcolor;
    const sf::Vector2<int>origin(fieldwidth / 2, 0);
    sf::Vector2<int>position(origin);
    sf::RenderWindow window(sf::VideoMode(windowwidth, windowheight), L"俄羅斯方塊");
    sf::Clock clock;
    window.setFramerateLimit(30);
    while (window.isOpen())
    {
        currentshape = shapes[currenttype][currentindex];
        currentcolor = sprites[currenttype];
        enum class Action
        {
            hold, down, left, right,rotation,
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
                switch (event.key.code)
                {
                case sf::Keyboard::Left:
                    action = Action::left;
                    break;
                case sf::Keyboard::Right:
                    action = Action::right;
                    break;
                case sf::Keyboard::Down:
                    action = Action::down;
                    break;
                case sf::Keyboard::Up:
                    action = Action::rotation;
                default:
                    break;
                }
            }
        }
        if (clock.getElapsedTime().asSeconds() >= 0.3f)
        {
            action = Action::down;//nextposition.y = nextposition.y + 1;
            clock.restart();
        }
        sf::Vector2<int>nextposition(position);
            int nextindex = currentindex;
            if (action == Action::rotation) 
            {
                nextindex = (nextindex + 1)%shapes[currenttype].size();
            }
            std::vector < sf::Vector2<int>>nextshape=shapes[currenttype][nextindex];
            switch (action)
            {
            case Action::hold:
                break;
            case Action::down:
                nextposition.y = nextposition.y + 1;
                break;
            case Action::left:
                nextposition.x = nextposition.x - 1;
                break;
            case Action::right:
                nextposition.x = nextposition.x + 1;
                break;
            case Action::rotation:

            default:
                break;
            }
            int countempty = 0;
            
            for (const sf::Vector2<int>distance : nextshape)
            {
                sf::Vector2<int>nextposition2 = nextposition + distance;
                if (nextposition2.x >= 0 && nextposition2.x < fieldwidth &&
                    nextposition2.y < fieldhight && (nextposition2.y<0||field[nextposition2.x][nextposition2.y] == type::None))
                {
                    countempty++;
                }
            }
            if (countempty==4)
            {
                position = nextposition;
                currentindex = nextindex;
                currentshape = nextshape;
            }
            else
            {
                if (action==Action::down)
                {
                    for (const sf::Vector2<int>& distance : currentshape)
                    {
                        sf::Vector2<int>nextposition2 = position + distance;
                        if (nextposition2.y >= 0)
                        {
                            field[nextposition2.x][nextposition2.y] =currenttype;
                        }
                    }
                    for (int y = 0; y < fieldhight; y++)
                    {
                        bool isfull=true;
                        for (int x = 0; x < fieldwidth; x++)
                        {
                            if (field[x][y] == type::None)
                            {
                                isfull = false;
                            }
                        }
                        if (isfull == true)
                        {
                            for (int temp_y = y; temp_y > 0; temp_y--)
                            {
                                for (int x = 0; x < fieldwidth; x++)
                                {
                                    field[x][temp_y] = field[x][temp_y - 1];
                                }
                            }
                            for (int x = 0; x < fieldwidth; x++)
                            {
                                field[x][0] = type::None;
                            }
                        }
                    }
                    position = origin;
                    currenttype = type(rand() % 3+1);
                    currentindex = 0;
                }
            }
            window.clear();
            window.draw(backgroundsprite);
            //繪製背景
            for (int x = 0; x < fieldwidth; x++)
            {
                for (int y = 0; y < fieldhight; y++)
                {
                    if (field[x][y] == type::None) continue;
                    sf::Sprite& s = sprites[field[x][y]];
                    
                    s.setPosition(float(x * blockwidth), float(y * blockhight));
                    window.draw(s);
                    
                }
            }
            //繪製控制物體
            for (const sf::Vector2<int>& distance : currentshape)
            {
                sf::Vector2<int>nextposition2 = position + distance;
                currentcolor.setPosition(float(nextposition2.x* blockwidth), float(nextposition2.y* blockhight));
                window.draw(currentcolor);
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
