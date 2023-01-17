function Button({children, onClick, disabled=false}) {
    return <button className="bg-green-600 text-white button rounded p2 
    border my-1 hover:bg-blue-900 disabled:bg-gray-300 disabled:text-black"
    disabled={disabled}  
    onClick={onClick}>{children}</button>
  }

export default Button;  