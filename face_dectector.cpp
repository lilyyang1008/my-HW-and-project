// face_dectector.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/objdetect.hpp>
#include<opencv2/imgproc.hpp>
#include<iostream>

int main()
{
    cv::VideoCapture video("D:\\C++ project\\face_dectector\\face-demographics-walking-and-pause.mp4");
    cv::CascadeClassifier face_detector("D:\\C++ project\\face_dectector\\haarcascade_frontalface_alt.xml");
    
    while (true) {
        cv::Mat image;
        if (!video.read(image)) {
            break;
        }
        
        std::vector<cv::Rect>faces;
        face_detector.detectMultiScale(image, faces);
        for (const cv::Rect& face : faces)
        {
            cv::rectangle(image, face, cv::Scalar(0, 0, 255), 2);
            //std::cout << face.x << "," << face.y << std::endl;
        }
        std::vector<cv::Rect>bodys;
        
        cv::imshow("image", image);
        
        cv::waitKey(10);
    }
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
