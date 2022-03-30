%% Initialization
clear; close all; clc;

files = {"convergence_to_average_mk1_IS.txt"; 
	"convergence_to_average_mk1_RW.txt";
	"convergence_to_average_mk2_IS.txt"; 
	"convergence_to_average_mk2_RW.txt";
	"convergence_to_average_ms_IS.txt";
	"convergence_to_average_ms_RW.txt"};

title_stub = "Mean Number of Generations Attained, ";

title_caps = {"Monkey 1, IS";
	"Monkey 1, RW";
	"Monkey 2, IS"; 
	"Monkey 2, RW";
	"Mouse, IS";
	"Mouse, RW"};

out_stub = "convergence_to_average_";
out_caps = {"mk1_IS.png";
	"mk1_RW.png";
	"mk2_IS.png";
	"mk2_RW.png";
	"ms_IS.png";
	"ms_RW.png"}

colors = {[];[];[];[];[];[];[];[];[];[];[]};

for idx = 1:6
	data = load(files(idx, 1));
	
	y_max = max(max(data(:, 2:12))) + 1;

	plot_title = strcat(title_stub, title_caps(idx, 1));

	out_figure = figure("Units", "normalized", "Position", [0 0 1 1]);

	for j = 2:12
		plot(data(:,1), data(:, j), "color", colors(j, 1), "LineWidth", 2);
		hold on;
	endfor

	title(plot_title, "FontSize", 25);
	xlabel("Time Horizon", "FontSize", 16);
	ylabel("Mean", "FontSize", 16)
	legend("L = 1", "L = 10%", "L = 20%", "L = 30%", "L = 40%", "L = 50%", "L = 60%", "L = 70%", "L = 80%", "L = 90%", "L = 100%");
	ylim([0, y_max]);

	out_name = strcat(out_stub, out_caps(j, 1));

	saveas(out_figure, out_name)

endfor