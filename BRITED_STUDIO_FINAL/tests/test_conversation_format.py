import unittest

from leveria.audit import audit_script
from leveria.formats import FORMATS
from leveria.prompts import brief


class ConversationFormatTests(unittest.TestCase):
    def test_all_destinations_receive_the_conversation_brief(self):
        for platform, fmt in FORMATS.items():
            self.assertEqual((60, 65), (fmt.target_seconds_min, fmt.target_seconds_max))
            prompt = brief(platform, 'Exemple', 'concept', 'Source', {})
            self.assertIn('« vous »', prompt)
            self.assertIn('60 à 65 secondes', prompt)
            self.assertIn('chronométrer', prompt)
            self.assertNotIn('Aucune durée maximale', prompt)

    def test_outside_duration_range_requires_a_timed_read(self):
        for count in (60, 250):
            result = audit_script(' '.join(['mot'] * count), 'shorts')
            self.assertTrue(any('Durée indicative' in item for item in result.warnings))

    def test_tutoiement_and_useful_ending_without_cta(self):
        result = audit_script('Imagine que tu vérifies ton document. Regarde le montant indiqué.', 'shorts')
        self.assertFalse(any('projection' in item or 'réflexe pratique' in item for item in result.errors))
        self.assertFalse(any('appel à l’action' in item for item in result.warnings))


if __name__ == '__main__':
    unittest.main()
