interface Props {
  lane1: string;
  lane2: string;
}

const Occupancy = ({ lane1, lane2 }: Props) => {
  return (
    <div className="rounded-lg shadow-lg p-2 flex flex-col min-w-80 border border-gray-200">
      <div className="font-semibold text-black text-2xl">
        Lane Occupancy Rate:
      </div>
      <div className="flex justify-between gap-2">
        <div>
          <div className="font-semibold text-black text-xl">Lane 1:</div>
          <div className="font-mono text-black self-end text-3xl font-semibold">
            {lane1}
          </div>
        </div>
        <div>
          <div className="font-semibold text-black text-xl">Lane 2:</div>
          <div className="font-mono text-black self-end text-3xl font-semibold">
            {lane2}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Occupancy;
