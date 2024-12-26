import data_structs as DS


class Math:
    """Class for game-related conversions and calculations."""

    def __init__(self):
        """Initialize conversion management."""
        pass

    # Bespoke conversion methods
    def dec_to_pct(self, p_decimal: float) -> str:
        """Convert decimal to percentage."""
        return f"{round(p_decimal * 100, 5):,} %"

    def pct_to_dec(self, p_percent: str) -> float:
        """Convert percentage to decimal factor."""
        return round(float(p_percent.replace("%", "").strip()) / 100, 5)

    def diam_to_radius(self, p_diameter: float) -> float:
        """Convert diameter to radius."""
        return p_diameter / 2

    def radius_to_diam(self, p_radius: float) -> float:
        """Convert radius to diameter."""
        return round(p_radius * 2, 5)

    def convert(
        self, value: float, conversion_factor: float, p_round: bool = True
    ) -> float:
        """Generic conversion method."""
        result = value * conversion_factor
        return round(result, 5) if p_round else result

    # Conversions using the generic convert method
    def grams_to_kilos(self, p_grams: float, p_round: bool = True) -> float:
        """Convert grams to kilos."""
        return self.convert(p_grams, DS.GRAMS_TO_KILOS, p_round)

    def kilos_to_grams(self, p_kilos: float, p_round: bool = True) -> float:
        """Convert kilos to grams."""
        return self.convert(p_kilos, DS.KILOS_TO_GRAMS, p_round)

    def kilos_to_pounds(self, p_kilos: float, p_round: bool = True) -> float:
        """Convert kilos to pounds."""
        return self.convert(p_kilos, DS.KILOS_TO_POUNDS, p_round)

    def pounds_to_kilos(self, p_pounds: float, p_round: bool = True) -> float:
        """Convert pounds to kilos."""
        return self.convert(p_pounds, DS.POUNDS_TO_KILOS, p_round)

    def pounds_to_oz(self, p_pounds: float, p_round: bool = True) -> float:
        """Convert pounds to ounces."""
        return self.convert(p_pounds, DS.POUNDS_TO_OZ, p_round)

    def oz_to_pounds(self, p_oz: float, p_round: bool = True) -> float:
        """Convert ounces to pounds."""
        return self.convert(p_oz, DS.OZ_TO_POUNDS, p_round)

    def oz_to_grams(self, p_oz: float, p_round: bool = True) -> float:
        """Convert ounces to grams."""
        return self.convert(p_oz, DS.OZ_TO_GRAMS, p_round)

    def grams_to_oz(self, p_grams: float, p_round: bool = True) -> float:
        """Convert grams to ounces."""
        return self.convert(p_grams, DS.GRAMS_TO_OZ, p_round)

    def cm_to_inches(self, p_cm: float, p_round: bool = True) -> float:
        """Convert centimeters to inches."""
        return self.convert(p_cm, DS.CM_TO_INCHES, p_round)

    def inches_to_cm(self, p_inches: float, p_round: bool = True) -> float:
        """Convert inches to centimeters."""
        return self.convert(p_inches, DS.INCHES_TO_CM, p_round)

    def ft_to_meters(self, p_ft: float, p_round: bool = True) -> float:
        """Convert feet to meters."""
        return self.convert(p_ft, DS.FT_TO_METERS, p_round)

    def meters_to_ft(self, p_meters: float, p_round: bool = True) -> float:
        """Convert meters to feet."""
        return self.convert(p_meters, DS.METERS_TO_FT, p_round)

    def km_to_mi(self, p_km: float, p_round: bool = True) -> float:
        """Convert kilometers to miles."""
        return self.convert(p_km, DS.KM_TO_MI, p_round)

    def km_to_ka(self, p_km: float, p_round: bool = True) -> float:
        """Convert kilometers to katas."""
        return self.convert(p_km, DS.KM_TO_KA, p_round)

    def km_to_ga(self, p_km: float, p_round: bool = True) -> float:
        """Convert kilometers to gawos."""
        return self.convert(p_km, DS.KM_TO_GA, p_round)

    # Additional conversion methods based on your comments
    def in_to_mm(self, p_inches: float, p_round: bool = True) -> float:
        """Convert inches to millimeters."""
        return self.convert(p_inches, DS.IN_TO_MM, p_round)

    def mm_to_in(self, p_mm: float, p_round: bool = True) -> float:
        """Convert millimeters to inches."""
        return self.convert(p_mm, DS.MM_TO_IN, p_round)

    def cm_to_mm(self, p_cm: float, p_round: bool = True) -> float:
        """Convert centimeters to millimeters."""
        return self.convert(p_cm, DS.CM_TO_MM, p_round)

    def mm_to_cm(self, p_mm: float, p_round: bool = True) -> float:
        """Convert millimeters to centimeters."""
        return self.convert(p_mm, DS.MM_TO_CM, p_round)

    def km_to_m(self, p_km: float, p_round: bool = True) -> float:
        """Convert kilometers to meters."""
        return self.convert(p_km, DS.KM_TO_M, p_round)

    def m_to_km(self, p_m: float, p_round: bool = True) -> float:
        """Convert meters to kilometers."""
        return self.convert(p_m, DS.M_TO_KM, p_round)

    # Add more conversion methods here using the same pattern...
