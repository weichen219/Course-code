clc,clear

dist=[ 9999 107 241 190 124  80 316 ;
       107  9999 148 137  88 127 336 ;
       241 148  9999 374 171 259 509;
       190 137 374  9999 202 234 222;
       124  88 171 202  9999  61 392;
        80 127 259 234  61 9999 386;
       316 336 509 222 392 386 9999] ;

dist_size=size(dist) ; 
dist_size=dist_size(1,1) ;
C=[] ;
for i=1:dist_size
    C(i)=i ;
end
start_pos=1 ;
current_pos=start_pos ;
V=[];
V=union(current_pos,V) ;
C = setdiff(C,V) ;
total_dis=0 ;
witer=1 ;
recode_pos=zeros(1,dist_size) ;
recode_pos(1,witer)=start_pos ;

while numel(C)>0 
     u=numel(C) ;
     xy=zeros(2,u) ;
     iter=0 ;
     for i=C
         y=dist(current_pos,i) ;
         iter=iter+1 ;
         xy(1,iter)=iter ;
         xy(2,iter)=y ;
     end
    % min_dis=min(xy(2,:)) ;
     %[ne,u]=find(dist(:,current_pos)==min_dis) ;
     next_pos_test=current_pos 
     V=union(next_pos_test,V) 
     C_test = setdiff(C,V) 
     cal_ne=C_test(1,1)
     C_cal = setdiff(C,cal_ne)
     
      u=numel(C) 
      xu=zeros(u,u) 
     for i=C
         for j=C
         
         y=dist(i,j)
         xu(i,j)=y
         end   
     end
     min_dis=min(xy(2,:)) ;
     [ne,u]=find(dist(:,current_pos)==min_dis) ;
     next_pos=ne ;
     V=union(next_pos,V) ;
     C = setdiff(C,V) ;    
     witer=witer+1 ;
     recode_pos(1,witer)=next_pos;
     current_pos=next_pos ;
     total_dis=total_dis+min_dis ;
    
end
go_back_start=dist(current_pos,start_pos);
total_dis=total_dis+go_back_start ;

disp('城市旅遊順序')
disp(recode_pos)
disp('總距離')
disp(total_dis)
