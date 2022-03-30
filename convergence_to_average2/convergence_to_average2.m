%% Initialization
clear; close all; clc;

files = {"convergence_to_average_mk1_IS.txt"; 
	"convergence_to_average_mk1_RW.txt";
	"convergence_to_average_mk2_IS.txt"; 
	"convergence_to_average_mk2_RW.txt";
	"convergence_to_average_ms_IS.txt";
	"convergence_to_average_ms_RW.txt"};

title_stub = "Mean Number of Generations Attained, ";

title_caps = {" Monkey 1, IS";
	" Monkey 1, RW";
	" Monkey 2, IS"; 
	" Monkey 2, RW";
	" Mouse, IS";
	" Mouse, RW"};

out_stub = "convergence_to_average_";
out_caps = {"mk1_IS.png";
	"mk1_RW.png";
	"mk2_IS.png";
	"mk2_RW.png";
	"ms_IS.png";
	"ms_RW.png"};

colors = {[0.2039 0.4667 0.9216];
[0.2706 0.4706 0.8549];
[0.3333 0.4745 0.7922];
[0.4 0.4745 0.7255];
[0.4667 0.4784 0.6588];
[0.5294 0.4824 0.5961];
[0.5961 0.4863 0.5294];
[0.6588 0.4902 0.4667];
[0.7255 0.4941 0.4];
[0.7922 0.4941 0.3333];
[0.8549 0.498 0.2706];
[0.9216 0.502 0.2039]};

for idx = 1:6
  data = load(char(files(idx, 1)));
	
	y_max = max(max(data(:, 2:12))) + 1;
  
  plot_title = strcat(char(title_stub), char(title_caps(idx, 1)));
  
  out_figure = figure("Units", "normalized", "Position", [0 0 .9 .9]);
  
  title(plot_title, "FontSize", 25);
	xlabel("Time Horizon", "FontSize", 16);
	ylabel("Mean", "FontSize", 16);
  ylim([0, y_max]);

	
  hold on;

	for j = 2:12
		plot(data(:,1), data(:, j), "color", cell2mat(colors(j, 1)), "LineWidth", 1);
		hold on;
	end
  
  
	legend("L = 1", "L = 10%", "L = 20%", "L = 30%", "L = 40%", "L = 50%", "L = 60%", "L = 70%", "L = 80%", "L = 90%", "L = 100%");
	hold on;

	out_name = strcat(char(out_stub), char(out_caps(idx, 1)));

	saveas(out_figure, out_name);

endfor