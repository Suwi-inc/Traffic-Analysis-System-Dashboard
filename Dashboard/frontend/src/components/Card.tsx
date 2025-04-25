interface Props {
  title: string;
  item: string;
}

const Card = ({ title, item }: Props) => {
  return (
    <div className="rounded-lg shadow-lg p-2 flex flex-col min-w-80 border border-gray-200">
      <div className="font-semibold text-black text-3xl">{title}:</div>
      <div className="font-mono text-black self-end text-5xl font-semibold">
        {item}
      </div>
    </div>
  );
};

export default Card;
