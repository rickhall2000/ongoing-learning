const LanguageDropDown = ({value, callback}) => {
    return (
        <select value={value} onChange={(e) => callback(e.target.value) }>
            <option value="en">English</option>
            <option value="fr">French</option>
            <option value="de">German</option>
            <option value="es">Spanish</option>
        </select>
    )
}

export default LanguageDropDown;