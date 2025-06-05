interface Props {
  type_distribution: {
    [key: string]: {
      [key: string]: number;
    };
  };
}

const TypeDistribution = ({ type_distribution }: Props) => {
  return (
    <div className="rounded-lg shadow-lg p-2 flex flex-col min-w-80 border border-gray-200">
      <div className="font-semibold text-black text-2xl">
        Vehicle Type Distribution:
      </div>
      <div className="flex justify-between gap-2">
        {Object.entries(type_distribution).map((x) => (
          <div key={x[0]}>
            <div className="font-semibold text-black text-xl">{x[0]}:</div>
            <div className="flex gap-2">
              {Object.entries(x[1]).map((y) => (
                <>
                  <div key={y[0]} className="font-semibold text-black">
                    {y[0]}:
                  </div>
                  <div className="text-black font-semibold">{y[1]}</div>
                </>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TypeDistribution;
