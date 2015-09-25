%% Analyze randia users

B = cell(68668,1);
B{68668,1} = [];

for i=1:68668    
    B(i,1) = strcat(RandiaFullAnalysis(i,9), ',', RandiaFullAnalysis(i,10), ',', RandiaFullAnalysis(i,11), ... 
        ',', RandiaFullAnalysis(i,12), ',',  RandiaFullAnalysis(i,13), ',', RandiaFullAnalysis(i,14), ...
        ',', RandiaFullAnalysis(i,15), ',', RandiaFullAnalysis(i,16));
end