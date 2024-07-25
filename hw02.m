I=imread('pout.tif');
input=double(I);
[x_max,y_max]=size(input);
output=ones(x_max,y_max);
dither_matrix=[0 128;192 64];
for x=1:x_max
    for y=1:y_max
        i=mod(x,2);
        j=mod(y,2);
        while i==0
            i=i+2;
        end
        while j==0
            j=j+2;
        end
        if input(x,y)>=dither_matrix(i,j)
            output(x,y)=255;
        else
            output(x,y)=0;
        end
    end
end

imshow(output,[0 255])