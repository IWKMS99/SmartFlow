type ArticleCardProps = {
  title: string;
};

function ArticleCard({ title }: ArticleCardProps) {
  return (
    <div>
      <h3>{title}</h3>
    </div>
  );
}

export default ArticleCard;