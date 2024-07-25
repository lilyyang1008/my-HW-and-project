clear all
input=double(imread('lena.tif'));
subplot(2,2,1);
imshow(input,[0 255]);
title('original image')
[x_max,y_max]=size(input);
edge_detection=zeros(x_max,y_max);
edge_enhancement=zeros(x_max,y_max);
low_pass=zeros(x_max,y_max);
temp=zeros(x_max+2,y_max+2);
temp(2:x_max+1,2:y_max+1)=input; %pad with zeros
for x=2:x_max+1
    for y=2:y_max+1
        edge_detection(x-1,y-1)=temp(x-1,y-1)*0+temp(x-1,y)*(-1)+temp(x-1,y+1)*0+temp(x,y-1)*(-1)+temp(x,y)*4 ...,
            +temp(x,y+1)*(-1)+temp(x+1,y-1)*0+temp(x+1,y)*(-1)+temp(x+1,y+1)*0;
        edge_enhancement(x-1,y-1)=temp(x-1,y-1)*0+temp(x-1,y)*(-1)+temp(x-1,y+1)*0+temp(x,y-1)*(-1)+temp(x,y)*5 ...,
            +temp(x,y+1)*(-1)+temp(x+1,y-1)*0+temp(x+1,y)*(-1)+temp(x+1,y+1)*0;
        low_pass(x-1,y-1)=temp(x-1,y-1)/9+temp(x-1,y)/9+temp(x-1,y+1)/9+temp(x,y-1)/9+temp(x,y)/9 ...,
            +temp(x,y+1)/9+temp(x+1,y-1)/9+temp(x+1,y)/9+temp(x+1,y+1)/9;
    end
end
subplot(2,2,2);
imshow(edge_detection,[0 255]);
title('after edge detection filter')
subplot(2,2,3);
imshow(edge_enhancement,[0 255]);
title('after edge enhancement filter')
subplot(2,2,4);
imshow(low_pass,[0 255])
title('after low pass filter')