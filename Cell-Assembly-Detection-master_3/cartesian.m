function tbl = cartesian(varargin)
    names = arrayfun(@inputname, 1:nargin, 'UniformOutput', false);
    
    for i = 1:nargin
        if isempty(names{i})
            names{i} = ['var' num2str(i)];
        end
    end
    
    rev_args = flip(varargin);
    
    [A{1:nargin}] = ndgrid(rev_args{:});

    B = cellfun(@(x) x(:), A, 'UniformOutput', false);
    C = flip(B);
    
    tbl = table(C{:}, 'VariableNames', names);
end