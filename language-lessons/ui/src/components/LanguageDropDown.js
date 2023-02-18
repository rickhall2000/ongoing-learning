const LanguageDropDown = ({value, callback}) => {
    return (
        <div className="mx-2 my-2" >
        <select value={value} onChange={(e) => callback(e.target.value)}>
            <option value="en">English</option>
            <option value="fr">French</option>
            <option value="de">German</option>
            <option value="es">Spanish</option>
        </select>
        </div>
    )
}

export default LanguageDropDown;