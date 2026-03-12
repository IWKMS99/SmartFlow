type InputProps = {
  placeholder?: string;
};

function Input({ placeholder }: InputProps) {
  return (
    <input placeholder={placeholder} />
  );
}

export default Input;