interface Props {
  occupancy: {
    [key: string]: number;
  };
}

const Occupancy = ({ occupancy }: Props) => {
  return (
    <div className="rounded-lg shadow-lg p-2 flex flex-col min-w-80 border border-gray-200">
      <div className="font-semibold text-black text-2xl">
        Lane Occupancy Rate:
      </div>
      <div className="flex justify-between gap-2">
        {Object.entries(occupancy).map((x) => (
          <div key={x[0]}>
            <div className="font-semibold text-black text-xl">{x[0]}:</div>
            <div className="font-mono text-black self-end text-2xl font-semibold">
              {x[1]}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Occupancy;
