% 定义外部调用函数 inputDir 输入文件夹 outDir 输出文件夹 labelIDStr 输入ID字符串
function outFile = run(inputDir, outDir, labelIDStr)

% 清理环境
close all;

% 拼接图像目录
img_dir = fullfile(outDir, 'pictures_walet');
if ~exist(img_dir, 'dir')
    mkdir(img_dir);
    disp(['文件夹已创建', img_dir]);
else
    disp(['文件夹已存在', img_dir]);
end
outFile = fullfile(outDir, "classification_results_1.xlsx");
% 获取文件夹中所有数据文件
folder = inputDir;
fileTypes = {'*.txt', '*.xlsx', '*.csv'};
files = [];
for k = 1:length(fileTypes)
    filePattern = fullfile(folder, fileTypes{k});
    currentFiles = dir(filePattern);
    files = [files; currentFiles];
end

% 加载模型
load net.mat
net = optimizedNet;

fs = 20; % 数据采样频率
t = 0:1/fs:1200/fs;

labelNames = {'倾斜', '噪声', '平波', '方波', '次小', '正常', '漂移'};

strArray = split(labelIDStr, ",");
doubleArray = str2double(strArray);  % 先转双精度
selectedIdx = int32(doubleArray);      % 再转为整数类型
selectedLabels = labelNames(selectedIdx);

% 定义用于存放文件名和分类标签的数组
fileNames = cell(1440, 1);
labels = cell(1440, 1);


% 数据处理部分
for k = 1:length(files)
    baseFileName = files(k).name;
    fullFileName = fullfile(files(k).folder, baseFileName);
    [~, ~, ext] = fileparts(baseFileName);
    ext = lower(ext);

    try
        % 根据文件类型读取数据
        switch ext
            case '.txt'
                x = load(fullFileName);
            case {'.xlsx', '.xls'}
                x = readmatrix(fullFileName, 'Range', 'A1:A72000');
            case '.csv'
                data = readmatrix(fullFileName);
                x = data(1:72000, 1); % 第四列，行3-72002
            otherwise
                error('不支持的格式: %s', ext);
        end

        % 验证数据长度
        x = x(:); % 确保列向量
        if numel(x) ~= 72000
            error('数据长度错误，应为72000个数据点，实际为%d', numel(x));
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
            fileName = fullfile(img_dir, sprintf('%s_%02d_%02d.bmp', folderName, k-1, i));
            print(gcf, '-dbmp', fileName);
            fileNames{(k-1)*60 + i} = fileName;
            close(gcf);
        end
    catch ME
        warning('文件%s处理失败: %s', baseFileName, ME.message);
    end
end

% 分类及数据清洗
validCount = 1;
filteredFiles = cell(60*length(files),1);
filteredLabels = cell(60*length(files),1);


for i = 1:60*length(files)
    try
        if isempty(fileNames{i}), continue; end % 跳过空文件名

        img = imread(fileNames{i});
        resizedImg = imresize(img, [227 227]);
        [labelIdx, ~] = classify(optimizedNet, resizedImg);
        currentLabel = labelNames{labelIdx};

        if ismember(currentLabel, selectedLabels)
            filteredFiles{validCount} = fileNames{i};
            filteredLabels{validCount} = currentLabel;
            validCount = validCount + 1;
        end
    catch ME
        warning('文件%s处理失败: %s', fileNames{i}, ME.message);
    end
end

% 清理空元素并保存
filteredFiles = filteredFiles(1:validCount-1);
filteredLabels = filteredLabels(1:validCount-1);
resultsTable = table(filteredFiles, filteredLabels,...
                    'VariableNames', {'FileName', 'Label'});
writetable(resultsTable, outFile);

outFile

end