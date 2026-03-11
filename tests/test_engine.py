import unittest

from global_namecase_engine import NameCaseConfig, NameCaseEngine, normalize_name


class NameCaseEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = NameCaseEngine()

    def test_spanish_particle_phrase(self) -> None:
        self.assertEqual(self.engine.normalize("JUAN DE LA CRUZ"), "Juan de la Cruz")

    def test_dutch_particle_phrase(self) -> None:
        self.assertEqual(self.engine.normalize("LUDWIG VAN DER BERG"), "Ludwig van der Berg")

    def test_mc_prefix(self) -> None:
        self.assertEqual(self.engine.normalize("ROBERT MCCARTHY"), "Robert McCarthy")

    def test_apostrophe_titlecase(self) -> None:
        self.assertEqual(self.engine.normalize("O'CONNOR"), "O'Connor")

    def test_apostrophe_lowercase_prefix(self) -> None:
        self.assertEqual(self.engine.normalize("D'ANGELO"), "d'Angelo")

    def test_hyphenated_name(self) -> None:
        self.assertEqual(self.engine.normalize("ANNE-MARIE SMITH"), "Anne-Marie Smith")

    def test_initials(self) -> None:
        self.assertEqual(self.engine.normalize("R. NARAYANAN"), "R. Narayanan")

    def test_compound_initials(self) -> None:
        self.assertEqual(self.engine.normalize("J.R.R. TOLKIEN"), "J.R.R. Tolkien")

    def test_abbreviations_are_not_misread_as_initials(self) -> None:
        self.assertEqual(self.engine.normalize("ST. JOHN"), "St. John")

    def test_suffixes(self) -> None:
        self.assertEqual(self.engine.normalize("MARTIN LUTHER KING JR."), "Martin Luther King Jr.")
        self.assertEqual(self.engine.normalize("HENRY FORD III"), "Henry Ford III")

    def test_whitespace_and_unicode_apostrophe_cleanup(self) -> None:
        self.assertEqual(self.engine.normalize("  maria   d\u2019angelo  "), "Maria d'Angelo")

    def test_none_passthrough(self) -> None:
        self.assertIsNone(self.engine.normalize(None))

    def test_blank_string(self) -> None:
        self.assertEqual(self.engine.normalize("   "), "")

    def test_type_error_for_non_strings(self) -> None:
        with self.assertRaises(TypeError):
            self.engine.normalize(123)  # type: ignore[arg-type]

    def test_exception_map_override(self) -> None:
        engine = NameCaseEngine(
            config=NameCaseConfig(
                exceptions={
                    "macarthur": "MacArthur",
                    "devito": "DeVito",
                },
            )
        )
        self.assertEqual(engine.normalize("MACARTHUR"), "MacArthur")
        self.assertEqual(engine.normalize("DEVITO"), "DeVito")

    def test_leading_particles_are_configurable(self) -> None:
        default_engine = NameCaseEngine()
        configured_engine = NameCaseEngine(
            config=NameCaseConfig(lowercase_leading_particles=True)
        )
        self.assertEqual(default_engine.normalize("DE NIRO"), "De Niro")
        self.assertEqual(configured_engine.normalize("DE NIRO"), "de Niro")

    def test_convenience_function(self) -> None:
        self.assertEqual(normalize_name("JUAN DE LOS SANTOS"), "Juan de los Santos")


if __name__ == "__main__":
    unittest.main()
