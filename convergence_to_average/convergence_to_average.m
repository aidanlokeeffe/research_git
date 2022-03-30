%% Initialization
clear; close all; clc

% Function to generate file name
function file_name = file(L)
  file_name = strcat("convergence_to_average_", num2str(L));
  file_name = strcat(file_name, ".txt");
end

% Load data
for L = 0:10
  data = load(file(L));
  t = data(:, 1);
  mk1_IS = data(:, 2);
  mk1_RW = data(:, 3);
  mk2_IS = data(:, 4);
  mk2_RW = data(:, 5);
  ms_IS = data(:, 6);
  ms_RW = data(:, 7);
  y_max = max(max(data(:, 2:7))) + 1
  
  plot_title = strcat("Mean Number of Generations at Time of Extinction, L=", num2str(L))

  out_figure = figure("Units", "normalized", "Position", [0 0 1 1]);
  plot(t, mk1_IS, "color", [0.4660 0.6740 0.1880], "LineWidth", 2)
  hold on
  plot(t, mk1_RW, "color", [0 1 0], "LineWidth", 2)
  hold on
  plot(t, mk2_IS, "color", [1 0 0], "LineWidth", 2)
  hold on
  plot(t, mk2_RW, "color", [1 0 1], "LineWidth", 2)
  hold on
  plot(t, ms_IS, "color", [0 0.4470 0.7410], "LineWidth", 2)
  hold on
  plot(t, ms_RW, "color", [0.3010 0.7450 0.9330], "LineWidth", 2)
  hold on

  title(plot_title, "FontSize", 25)
  xlabel("Time", "FontSize", 16)
  ylabel("Mean Number of Generations", "FontSize", 16)
  legend("Monkey 1, IS", "Monkey 1, RW", "Monkey 2, IS", "Monkey 2, RW", "Mouse, IS", "Mouse, RW")
  ylim([0, y_max])
  
  out_name = strcat("convergence_to_average_", num2str(L));
  out_name = strcat(out_name, ".png")
  
  saveas(out_figure, out_name)
endfor