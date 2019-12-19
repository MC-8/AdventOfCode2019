classdef IntCode < matlab.System
    % Untitled Add summary here
    %
    % This template includes the minimum set of functions required
    % to define a System object with discrete state.

    % Public, tunable properties
    properties
    output
    ipc
    opn
    setting
    done
    gi
    inp_idx
    instance_nr
    puzzle_input% = [3,8,1001,8,10,8,105,1,0,0,21,34,43,64,85,98,179,260,341,422,99999,3,9,1001,9,3,9,102,3,9,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,1001,9,2,9,1002,9,4,9,1001,9,3,9,1002,9,4,9,4,9,99,3,9,1001,9,3,9,102,3,9,9,101,4,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99];
    relbaseoffset
    full_input_sequence
    end

    properties(DiscreteState)

    end

    % Pre-computed constants
    properties(Access = private)

    end
    
    methods(Access = public)

    function obj = IntCode(varargin)
        % Support name-value pair arguments when constructing the
        % object.
        setProperties(obj,nargin,varargin{:});
    end

    function setInput(obj,u)
        obj.full_input_sequence = u;
    end
    
    end
    
    methods(Access = protected)

        function setupImpl(obj,u)
            obj.gi(1) = obj.setting;
            obj.gi(2) = u;
            obj.inp_idx = 1;
            obj.ipc = 1;
            obj.done = false;
            obj.relbaseoffset = 0;
            obj.opn{1}.fun = @obj.mysum      ; obj.opn{1}.nparam = 3; obj.opn{1}.nparamout = 1; obj.opn{1}.opcode = '1'; obj.opn{1}.fname = "mysum";
            obj.opn{2}.fun = @obj.mymul      ; obj.opn{2}.nparam = 3; obj.opn{2}.nparamout = 1; obj.opn{2}.opcode = '2'; obj.opn{2}.fname = "mymul";
            obj.opn{3}.fun = @obj.myinput    ; obj.opn{3}.nparam = 1; obj.opn{3}.nparamout = 1; obj.opn{3}.opcode = '3'; obj.opn{3}.fname = "myinput";
            obj.opn{4}.fun = @obj.myoutput   ; obj.opn{4}.nparam = 1; obj.opn{4}.nparamout = 1; obj.opn{4}.opcode = '4'; obj.opn{4}.fname = "myoutput";
            obj.opn{5}.fun = @obj.jumpiftrue ; obj.opn{5}.nparam = 2; obj.opn{5}.nparamout = 0; obj.opn{5}.opcode = '5'; obj.opn{5}.fname = "jumpiftrue";
            obj.opn{6}.fun = @obj.jumpiffalse; obj.opn{6}.nparam = 2; obj.opn{6}.nparamout = 0; obj.opn{6}.opcode = '6'; obj.opn{6}.fname = "jumpiffalse";
            obj.opn{7}.fun = @obj.lessthan   ; obj.opn{7}.nparam = 3; obj.opn{7}.nparamout = 1; obj.opn{7}.opcode = '7'; obj.opn{7}.fname = "lessthan";
            obj.opn{8}.fun = @obj.equals     ; obj.opn{8}.nparam = 3; obj.opn{8}.nparamout = 1; obj.opn{8}.opcode = '8'; obj.opn{8}.fname = "equals";
            obj.opn{9}.fun = @obj.addtorelbaseoffs      ; obj.opn{9}.nparam = 1; obj.opn{9}.nparamout = 0; obj.opn{9}.opcode = '9'; obj.opn{9}.fname = "addtorelbaseoffs";
            %%fprintf("Setup amp %d\n", obj.instance_nr);
        end

        function output = stepImpl(obj,u)
            % Implement algorithm. Calculate y as a function of input u and
            % discrete states.
            obj.gi(2) = u;
            output = obj.output;
            %fprintf("IPC=%d\n",obj.ipc);#
            while (and(obj.ipc < numel(obj.puzzle_input), not(obj.checkstop(obj.puzzle_input(obj.ipc)))))
                % Indexes
                opcode_word = num2str(obj.puzzle_input(obj.ipc)); obj.ipc=obj.ipc+1;
                % Pad if needed, simplifies mode selection
                if length(opcode_word)<5
                    opcode_word = pad(opcode_word,5,'left','0');
                end
                opcode = num2str(str2double(opcode_word(end-1:end))); %makes '02' to '2'
                opnpar = obj.getnparam(obj.opn,opcode);
                opnparout = obj.getnparamout(obj.opn,opcode);
                opnfun = obj.getopfun(obj.opn,opcode);
                par = [];
                % Parse parameter values and modes, incrementing program counter as it goes
                for k = 1:opnpar
                    par(k).mode = opcode_word(end-1-k);
                    par(k).val = obj.puzzle_input(obj.ipc);
                    obj.ipc=obj.ipc+1;
                    %fprintf("IPC=%d\n",obj.ipc);
                    %fprintf("Parameter %d: mode=%s, val=%d\n", k, par(k).mode, par(k).val);
                end

                % Get parameter values depending on their mode
                opval=[];
                for k = 1:opnpar%-opnparout % Only input parameters are relevant for modes
                    if (par(k).mode=='0') %position
                        opval(k) = obj.puzzle_input(zb2ob(par(k).val));
                    elseif (par(k).mode=='1') %immediate
                        opval(k) = par(k).val;
                    elseif (par(k).mode=='2') %relative
                        opval(k) = obj.puzzle_input(zb2ob(obj.relbaseaddr(par(k).val)));
                    else
                        disp("MODE NOT RECOGNISED")
                    end
                end

                % Deal array of values as tuple of arguments. Pass only input arguments
                if isempty(opval)
                    result = opnfun();
                else
                    args = mat2cell(opval(1:opnpar-opnparout),1,ones(1,numel(opval(1:opnpar-opnparout))));
                    result = opnfun(args{:});
                end
                % %fprintf("Opcode is %s\n",opcode);
                % %fprintf("Result is %d\n",result);
                % %fprintf("IPC is %d\n",obj.ipc);
  
                % Deal with outputs

                %fprintf("With opcode %s, output mode %s, result = %d", opcode, par(end).mode, result);
                if (opcode == '1') || (opcode == '2') || (opcode == '3') || (opcode == '7')|| (opcode == '8')
                    % Store input at a certain location
                    if par(end).mode=='0'
                        obj.puzzle_input(zb2ob(par(end).val)) = result;
                    elseif par(end).mode=='1'
                        disp(['INVALID OUTPUT MODE FOR OPCODE ' opcode])
                    elseif par(end).mode=='2'
                        obj.puzzle_input(zb2ob(obj.relbaseaddr(par(end).val))) = result;
                    end
                elseif opcode == '4' % The output instruction
                    if par(end).mode=='0'
                        obj.output = obj.puzzle_input(zb2ob(par(end).val));
                    elseif par(end).mode=='1'
                        obj.output = par(end).val;
                    elseif par(end).mode=='2'
                        obj.output = obj.puzzle_input(zb2ob(obj.relbaseaddr(par(end).val)));
                    end
                    output = obj.output;
                    return
                elseif (opcode == '5') || (opcode == '6') || (opcode == '9')
                    % These instructions have no output
                else
                    disp("OPCODE output not implemented")
                end
                output = obj.output;
            end
        end

        function resetImpl(obj)
            % Initialize / reset discrete-state properties
        end
                
        function opfun = getopfun(obj,opn,opcode)
        for i = 1:length(opn)
            if opn{i}.opcode==opcode
                opfun = opn{i}.fun;
            end
        end
        end

        function opparam = getnparam(obj,opn,opcode)
        for i = 1:length(opn)
            if opn{i}.opcode==opcode
                opparam = opn{i}.nparam;
            end
        end
        end

        function opparamout = getnparamout(obj,opn,opcode)
        for i = 1:length(opn)
            if opn{i}.opcode==opcode
                opparamout = opn{i}.nparamout;
            end
        end
        end

        function s = mysum(obj,a,b)
        %fprintf("mysum(%d,%d)\n",a,b);
        s = a+b;
        end

        function m = mymul(obj,a,b)
        %fprintf("mymul(%d,%d)\n",a,b);
        m = a*b;
        end

        function i = myinput(obj)
        %fprintf("Called myinput\n");
        if not(isempty(obj.full_input_sequence))
            i = obj.full_input_sequence(obj.inp_idx);
            obj.inp_idx = obj.inp_idx + 1;
        else
            i = obj.gi(obj.inp_idx);
            obj.inp_idx  = 2;
        end
        %fprintf("%d\n",i);
        end

        function dummy = myoutput(obj)
        dummy = -1; % Dummy. Output is set outside
        end

        function dummy = jumpiftrue(obj,par,ipn)
        %fprintf("jumpiftrue(%d,%d)\n",par,ipn);
        if (par)
            obj.ipc = zb2ob(ipn);
        end
        dummy = -1;
        end

        function dummy = jumpiffalse(obj,par,ipn)
        if not(par)
            obj.ipc = zb2ob(ipn);
        end
        dummy = -1;
        end

        function res = lessthan(obj,a,b)
        res = double(a<b);
        end

        function res = equals(obj,a,b)
        %fprintf("equals(%d,%d)\n",a,b);
        res = double(a==b);
        end

        function s = checkstop(obj,val)
        s = val==99;
        obj.done = s;
        end

        function b = zb2ob(obj,index)
        b = index +1;
        end
        
        function a = relbaseaddr(obj,index)
        a = index + obj.relbaseoffset;
        end

        function dummy = addtorelbaseoffs(obj,offs)
        obj.relbaseoffset = obj.relbaseoffset + offs;
        dummy = -1;
        end
    end
end


