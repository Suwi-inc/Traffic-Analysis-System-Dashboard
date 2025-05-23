interface Props {
  lane1: {
    [key: string]: number;
  };
  lane2: {
    [key: string]: number;
  };
}

const TypeDistribution = ({ lane1, lane2 }: Props) => {
  const lane1Entries = Object.entries(lane1);
  const lane2Entries = Object.entries(lane2);

  return (
    <div className="rounded-lg shadow-lg p-2 flex flex-col min-w-80 border border-gray-200">
      <div className="font-semibold text-black text-2xl">
        Vehicle Type Distribution:
      </div>
      <div className="flex justify-between gap-2">
        <div>
          <div className="font-semibold text-black text-xl">Lane 1:</div>
          {lane1Entries.map((x) => (
            <div key={x[0]} className="flex gap-2">
              <div className="font-semibold text-black text-xl">{x[0]}:</div>
              <div className="text-black text-xl font-semibold">{x[1]}</div>
            </div>
          ))}
        </div>
        <div>
          <div className="font-semibold text-black text-xl">Lane 1:</div>
          <div>
            {lane2Entries.map((x) => (
              <div key={x[0]} className="flex gap-2">
                <div className="font-semibold text-black text-xl">{x[0]}:</div>
                <div className="text-black text-xl font-semibold">{x[1]}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TypeDistribution;
