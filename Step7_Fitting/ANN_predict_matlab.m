function output=ANN_predict_matlab(input, SDS_choosed, net)
    num_SDS=3; % number of SDS, also number of pretrained models
    assert(max(SDS_choosed)<=num_SDS,'SDS number Error!');
    spec = predict(net, input);
    spec = normalize_spec(spec,2);
    output = spec;
end

function output=normalize_spec(input,direction)
    if direction==1
%         output=log10(input);
            output=-log(input);
    elseif direction==2
%         output=power(10,-input);
        output=exp(-input);
    else
        assert(false,'Function ''normalize_spec'' param ''direction'' Error!');
    end
end

function output=normalize_param(input,direction,nor)
    if direction==1
        mea= mean(input);
        st=std(input);
        output=(input-mea)./st;
        nor=[mea;st];
    elseif direction==2
        output=(input-nor(1,:))./nor(2,:);
    else
        assert(false,'Function ''normalize_spec'' param ''direction'' Error!');
    end
end