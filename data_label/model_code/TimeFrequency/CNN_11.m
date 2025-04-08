% 清理环境
clear;
close all;

% 获取文件夹中所有数据文件
folder = 'E:\桌面\苏通大桥\ZD020102';
fileTypes = {'*.txt', '*.xlsx', '*.csv'};
files = [];
for k = 1:length(fileTypes)
    filePattern = fullfile(folder, fileTypes{k});
    currentFiles = dir(filePattern);
    files = [files; currentFiles];
end

load net.mat; % 调用CNN分类模型

fs = 20; % 数据采样频率
t = 0:1/fs:1200/fs;

% 定义用于存放文件名和分类标签的数组
fileNames = cell(1440, 1);
labels = cell(1440, 1);

% 获取模型类别名称
classNames = net.Layers(end).ClassNames;

% 人工交互选择标签类别
selectedIdx = listdlg('ListString', classNames,...
                     'PromptString','请选择2-7个要保留的类别:',...
                     'SelectionMode','multiple',...
                     'ListSize',[300 200]);

% 验证选择数量
while isempty(selectedIdx) || numel(selectedIdx)<2 || numel(selectedIdx)>7
    errordlg('必须选择2-7个类别！', '选择错误');
    selectedIdx = listdlg('ListString', classNames,...
                         'PromptString','请选择2-7个要保留的类别:',...
                         'SelectionMode','multiple',...
                         'ListSize',[300 200]);
end
selectedClasses = classNames(selectedIdx);
disp(['已选择类别：' strjoin(selectedClasses', ', ')]);

% 数据处理部分
for k = 1:length(files)
    baseFileName = files(k).name;
    fullFileName = fullfile(files(k).folder, baseFileName);
    [~, ~, ext] = fileparts(baseFileName);
    ext = lower(ext);
    
    % 根据文件类型读取数据
    try
        switch ext
            case '.txt'
                x = load(fullFileName);
            case {'.xlsx', '.xls'}
                x = readmatrix(fullFileName, 'Range', 'D3:D72002');
            case '.csv'
                data = readmatrix(fullFileName);
                x = data(3:72002, 4); % 第四列，行3-72002
            otherwise
                error('不支持的格式: %s', ext);
        end
        
        x = x(:); % 确保列向量
        if numel(x) ~= 72000
            error('数据长度错误');
        end
        
        for i = 1:60
            % 正确提取1200个样本点
            startIdx = (i-1)*1200 + 1;
            endIdx = i*1200;
            data = x(startIdx:endIdx);
            
            % 连续小波变换
            wavename = 'cmor3-3';
            totalscal = 1024;
            Fc = centfrq(wavename);
            c = 2 * Fc * totalscal;
            scals = c ./ (1:totalscal);
            f = scal2frq(scals, wavename, 1/fs);
            coefs = cwt(data, scals, wavename);

            figure;
            imagesc(t, f, abs(coefs));
            set(gcf, 'unit', 'centimeters', 'position', [10 5 3 2]);
            set(gca, 'position', [0 0 1 1]);
            axis([0 1200/fs 0 5]);
            set(gca, 'YDir', 'normal');
            axis off;

            % 保存图像
            set(gcf, 'color', [1,1,1]);
            figWidth = 3.045;
            figHeight = 1.93;
            set(gcf, 'PaperUnits', 'centimeters');
            set(gcf, 'PaperPosition', [0 0 figWidth figHeight]);
            
            folderName = 'ZD020102_data';
            fileName = sprintf('E:\\桌面\\苏通大桥\\pictures_walet\\%s_%02d_%02d.bmp',...
                              folderName, k-1, i);
            print(gcf, '-dbmp', fileName);
            fileNames{(k-1)*60+i} = fileName;
            close(gcf);
        end
    catch ME
        warning('文件%s处理失败: %s', baseFileName, ME.message);
        continue;
    end
end

% 分类及数据清洗
validCount = 1;
filteredFiles = cell(1440,1);
filteredLabels = cell(1440,1);

progressBar = waitbar(0,'正在处理数据...'); % 添加进度条

for i = 1:1440
    try
        I = imread(fileNames{i});
        [label, ~] = classify(net, I);
        
        if ismember(char(label), selectedClasses)
            filteredFiles{validCount} = fileNames{i};
            filteredLabels{validCount} = char(label);
            validCount = validCount + 1;
        end
        
        % 更新进度条
        waitbar(i/1440, progressBar,...
            sprintf('已完成 %.1f%%，已找到%d有效数据',...
            i/1440*100, validCount-1));
    catch ME
        warning('文件%s处理失败: %s', fileNames{i}, ME.message);
    end
end

close(progressBar); % 关闭进度条

% 清理空元素并保存
filteredFiles = filteredFiles(1:validCount-1);
filteredLabels = filteredLabels(1:validCount-1);

resultsTable = table(filteredFiles, filteredLabels,...
                    'VariableNames', {'FileName', 'Label'});
writetable(resultsTable, 'E:\桌面\苏通大桥\custom_filter_results.xlsx');

% 显示最终统计
disp('========== 处理完成 ==========');
disp(['总数据量：' num2str(1440)]);
disp(['有效数据量：' num2str(height(resultsTable))]);
disp(['数据保留率：' num2str(height(resultsTable)/1440*100, '%.1f') '%']);
disp(['输出文件：custom_filter_results2.xlsx']);