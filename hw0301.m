clear all
i=imread('lena.tif');
I=double(i);
[xmax,ymax]=size(I);
O=zeros(xmax,ymax);
for x=1:xmax
    for y=1:ymax
        if I(x,y)<128
            O(x,y)=255-I(x,y);
        else
            O(x,y)=I(x,y);
        end
    end
end
O2=zeros(xmax,ymax);
for x=1:xmax
    for y=1:ymax
        if I(x,y)>128
            O2(x,y)=255-I(x,y);
        else
            O2(x,y)=I(x,y);
        end
    end
end
subplot(1,3,1);
imshow(I,[0 255]);
title('original image')
subplot(1,3,2);
imshow(O,[0 255]);
title('complementing only dark pixel')
subplot(1,3,3);
imshow(O2,[0 255]);
title('complementing only light pixel')