filename = 'space_blast.gif';
figure()
for i = 1:size(space_snapshot,2)
    space_mat{i} = ascii2bitmap(space_snapshot{i});
    h = image(space_mat{i});
    drawnow;
end

function a2b = ascii2bitmap(space_ascii)
space_mat = zeros(size(space_ascii,2),size(space_ascii,1),3);
for c=1:size(space_ascii,2)
    for r=1:size(space_ascii,1)
        if space_ascii(r,c)=='#'
            space_mat(r,c,:) = [1,0,0];
        elseif space_ascii(r,c)=='.'
            space_mat(r,c,:) = [0,0,0];
        elseif space_ascii(r,c)=='+'
            space_mat(r,c,:) = [0.05,0.05,0.05];
        elseif space_ascii(r,c)=='O'
            space_mat(r,c,:) = [0,1,0];
        elseif space_ascii(r,c)=='!'
            space_mat(r,c,:) = [0,0,1];            
        end
    end
end
a2b = space_mat;
end